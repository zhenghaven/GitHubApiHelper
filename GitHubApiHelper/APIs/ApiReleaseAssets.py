#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


import hashlib
import logging
import os
import requests

from ..DefaultHosts import DefaultApiHost, HostGetter
from ..Utils import CheckResp, LogEnvVars
from .ApiRunner import ApiRunner
from .ApiRelease import GetByTag as _GetByTag
from ._Types import (
	_AuthType,
	_ArgsType,
	_ArgParserType,
	_RespType,
)


class Get(ApiRunner):
	# https://docs.github.com/en/rest/releases/assets#get-a-release-asset

	URL_BASE = 'https://{api_host}/repos/{owner}/{repo}/releases/assets/{asset_id}'

	def __init__(
		self,
		owner: str,
		repoName: str,
		assetId: int,
		isDownload: bool,
		hostGetter: HostGetter = DefaultApiHost(),
	) -> None:
		super(Get, self).__init__()

		self._url = self.URL_BASE.format(
			api_host=hostGetter.GetHost(),
			owner=owner,
			repo=repoName,
			asset_id=assetId,
		)

		self._isDownload = isDownload

	def MakeRequest(self, auth: _AuthType) -> _RespType:
		authHeaderKey, authHeaderVal = auth.GetHeader()

		headers = {
			authHeaderKey: authHeaderVal,
		}
		if self._isDownload:
			headers['Accept'] = 'application/octet-stream'
		else:
			headers['Accept'] = 'application/vnd.github+json'

		req = requests.get(
			url=self._url,
			headers=headers,
			allow_redirects=True,
		)
		CheckResp.CheckRespErr(req)

		return req


class Download(ApiRunner):

	def __init__(
		self,
		owner: str,
		repoName: str,
		tag: str,
		assetName: str,
		savePath: os.PathLike,
		hostGetter: HostGetter = DefaultApiHost(),
	) -> None:
		super(Download, self).__init__()

		self._owner = owner
		self._repoName = repoName
		self._tag = tag
		self._assetName = assetName
		self._savePath = savePath
		self._hostGetter = hostGetter

		self._logger = logging.getLogger(__name__ + '.' + self.__class__.__name__)

	def CliRun(self, auth: _AuthType) -> None:
		# 1. get release info
		releaseGetter = _GetByTag(
			owner=self._owner,
			repoName=self._repoName,
			tag=self._tag,
			hostGetter=self._hostGetter,
		)
		release = releaseGetter.MakeRequest(auth).json()

		# 2. find asset id
		if 'assets' not in release:
			raise RuntimeError('No assets found in release')
		assetId = None
		for asset in release['assets']:
			if asset['name'] == self._assetName:
				assetId = asset['id']
				break
		if assetId is None:
			raise RuntimeError('Asset not found in release')
		self._logger.info(
			f'Asset named "{self._assetName}" found with id {assetId}'
		)

		# 3. download asset
		downloader = Get(
			owner=self._owner,
			repoName=self._repoName,
			assetId=assetId,
			isDownload=True,
			hostGetter=self._hostGetter,
		)
		fileContent = downloader.MakeRequest(auth).content

		self._logger.debug('Received {} bytes'.format(len(fileContent)))

		fileHash = hashlib.sha256(fileContent).hexdigest()
		self._logger.debug('SHA256: {}'.format(fileHash))

		with open(self._savePath, 'wb') as f:
			f.write(fileContent)
		self._logger.debug('Saved to {}'.format(self._savePath))

		print(fileHash)

	@staticmethod
	def _AddOpArgParsers(opArgParser: _ArgParserType) -> None:
		opArgParser.add_argument(
			'--version', '-v', type=str, required=True,
			help='Version of the release',
		)
		opArgParser.add_argument(
			'--asset', type=str, required=True,
			help='Name of the asset to download',
		)
		opArgParser.add_argument(
			'--save-path', '-o', type=os.path.abspath, required=True,
			help='Path to save the downloaded asset',
		)
		opArgParser.add_argument(
			'--repo', type=str, required=False,
			default=os.environ.get('GITHUB_REPOSITORY', None),
			help='Repo specified in the format of "owner/repo"'
				' (default: GITHUB_REPOSITORY env var)',
		)
		LogEnvVars.LogEnvVars()

	@classmethod
	def FromArgs(cls, args: _ArgsType) -> ApiRunner:
		if args.repo is None:
			raise ValueError('Repo not specified')

		owner, repoName = args.repo.split('/', maxsplit=1)

		return cls(
			owner=owner,
			repoName=repoName,
			tag=args.version,
			assetName=args.asset,
			savePath=args.save_path,
		)
