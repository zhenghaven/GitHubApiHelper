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

from typing import Union

from ..DefaultHosts import DefaultGhHost, HostGetter
from ..Utils import CheckResp
from .ApiRunner import ApiRunner
from ._Types import (
	_AuthType,
	_ArgsType,
	_ArgParserType,
	_RespType,
)


class DownloadAsset(ApiRunner):
	URL_BASE = 'https://{gh_host}/{owner}/{repo}/releases/download/{version}/{asset}'

	def __init__(
		self,
		owner: str,
		repoName: str,
		version: str,
		assetName: str,
		savePath: Union[os.PathLike, None],
		hostGetter: HostGetter = DefaultGhHost(),
	) -> None:
		super(DownloadAsset, self).__init__()

		self._url = self.URL_BASE.format(
			gh_host=hostGetter.GetHost(),
			owner=owner,
			repo=repoName,
			version=version,
			asset=assetName,
		)

		self._logger = logging.getLogger(__name__ + '.' + self.__class__.__name__)
		self._savePath = savePath

	def MakeRequest(self, auth: _AuthType) -> _RespType:
		authHeaderKey, authHeaderVal = auth.GetHeader()

		req = requests.get(
			url=self._url,
			headers={
				'Accept': 'application/octet-stream',
				authHeaderKey: authHeaderVal,
			},
		)
		CheckResp.CheckRespErr(req)

		return req

	def CliRun(self, auth: _AuthType) -> None:
		resp = self.MakeRequest(auth)

		fileContent = resp.content
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

	@classmethod
	def FromArgs(cls, args: _ArgsType) -> ApiRunner:
		if args.repo is None:
			raise ValueError('Repo not specified')

		owner, repoName = args.repo.split('/', maxsplit=1)

		return cls(
			owner=owner,
			repoName=repoName,
			version=args.version,
			assetName=args.asset,
			savePath=args.save_path,
		)
