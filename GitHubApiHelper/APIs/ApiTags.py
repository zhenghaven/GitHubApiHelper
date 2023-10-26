#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


import json
import os
import sys
import requests

from packaging import version
from typing import List

from ..DefaultHosts import DefaultApiHost, HostGetter
from ..Utils import CheckResp
from .ApiRunner import ApiRunner
from ._Types import (
	_ArgParserType,
	_ArgsType,
	_AuthType,
	_RespType,
)


class GetTagList(ApiRunner):
	# https://docs.github.com/en/rest/releases/releases#get-a-release-by-tag-name

	URL_BASE = 'https://{api_host}/repos/{owner}/{repo}/tags'

	def __init__(
		self,
		owner: str,
		repoName: str,
		hostGetter: HostGetter = DefaultApiHost(),
	) -> None:
		super(GetTagList, self).__init__()

		self._url = self.URL_BASE.format(
			api_host=hostGetter.GetHost(),
			owner=owner,
			repo=repoName,
		)

	def MakeRequest(self, auth: _AuthType) -> _RespType:
		headers = {
			'Accept': 'application/vnd.github+json',
		}

		if not auth.IsPublic():
			authHeaderKey, authHeaderVal = auth.GetHeader()
			headers[authHeaderKey] = authHeaderVal

		req = requests.get(
			url=self._url,
			headers=headers,
		)
		CheckResp.CheckRespErr(req)

		return req

	def CliRun(self, auth: _AuthType) -> None:
		resJson = self.MakeRequest(auth).json()
		print(json.dumps(resJson, indent='\t'))

	@staticmethod
	def _AddOpArgParsers(opArgParser: _ArgParserType) -> None:
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
		)


class GetLatestVer(GetTagList):

	def __init__(
		self,
		owner: str,
		repoName: str,
		localVers: List[str],
		isGitHubOut: bool = False,
		hostGetter: HostGetter = DefaultApiHost(),
	) -> None:
		super(GetLatestVer, self).__init__(
			owner=owner,
			repoName=repoName,
			hostGetter=hostGetter,
		)
		self.localVers = localVers
		self.isGitHubOut = isGitHubOut

	def CliRun(self, auth: _AuthType) -> None:
		if self.isGitHubOut and os.environ.get('GITHUB_OUTPUT', None) is None:
			raise RuntimeError('GitHub output is enabled but GITHUB_OUTPUT is not set')

		resJson = self.MakeRequest(auth).json()
		remoteVers = [tag['name'] for tag in resJson]

		# version object from packaging.version
		remoteVers = [version.parse(ver) for ver in remoteVers]
		localVers = [version.parse(ver) for ver in self.localVers]

		# version string from packaging.version
		remoteMaxVer = max(remoteVers)
		allMaxVer = max(remoteMaxVer, *localVers)
		lines = [
			f'remote={remoteMaxVer}\n',
			f'all={allMaxVer}\n',
		]

		# version string starting with 'v'
		remoteMaxVerStr = f'{remoteMaxVer}'
		remoteMaxVerStr = f'v{remoteMaxVerStr}' if not remoteMaxVerStr.startswith('v') else remoteMaxVerStr
		allMaxVerStr = f'{allMaxVer}'
		allMaxVerStr = f'v{allMaxVerStr}' if not allMaxVerStr.startswith('v') else allMaxVerStr
		lines.extend([
			f'remoteV={remoteMaxVerStr}\n',
			f'allV={allMaxVerStr}\n',
		])

		sys.stdout.writelines(lines)

		if self.isGitHubOut:
			with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
				f.writelines(lines)

	@staticmethod
	def _AddOpArgParsers(opArgParser: _ArgParserType) -> None:
		opArgParser.add_argument(
			'--repo', type=str, required=False,
			default=os.environ.get('GITHUB_REPOSITORY', None),
			help='Repo specified in the format of "owner/repo"'
				' (default: GITHUB_REPOSITORY env var)',
		)
		opArgParser.add_argument(
			'--local-ver', '-l', type=str, nargs='*', default=[],
			help='Local version string to compare with',
		)
		opArgParser.add_argument(
			'--github-out', action='store_true',
			help='Output to GitHub Actions',
		)

	@classmethod
	def FromArgs(cls, args: _ArgsType) -> ApiRunner:
		if args.repo is None:
			raise ValueError('Repo not specified')

		owner, repoName = args.repo.split('/', maxsplit=1)

		return cls(
			owner=owner,
			repoName=repoName,
			localVers=args.local_ver,
			isGitHubOut=args.github_out,
		)
