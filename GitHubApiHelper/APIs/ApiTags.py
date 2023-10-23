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
import requests

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
