#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


import base64
import os
import requests

from ..DefaultHosts import DefaultApiHost, HostGetter
from ..Utils import CheckResp, LogEnvVars
from .ApiRunner import ApiRunner
from ._Types import (
	_AuthType,
	_ArgsType,
	_ArgParserType,
	_RespType,
)


class CreateOrUpdate(ApiRunner):
	#https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#create-or-update-file-contents

	URL_BASE = 'https://{api_host}/repos/{owner}/{repo}/contents/{path}'

	def __init__(
		self,
		owner: str,
		repoName: str,
		destPath: str,
		commitMsg: str,
		contentBase64: str,
		branch: str = None,
		sha: str = None,
		hostGetter: HostGetter = DefaultApiHost(),
	) -> None:
		super(CreateOrUpdate, self).__init__()

		self._url = self.URL_BASE.format(
			api_host=hostGetter.GetHost(),
			owner=owner,
			repo=repoName,
			path=destPath,
		)

		self._body = {
			'message': commitMsg,
			'content': contentBase64,
		}
		if branch is not None:
			self._body['branch'] = branch
		if sha is not None:
			self._body['sha'] = sha

	def MakeRequest(self, auth: _AuthType) -> _RespType:
		authHeaderKey, authHeaderVal = auth.GetHeader()

		req = requests.put(
			url=self._url,
			headers={
				'Accept': 'application/vnd.github+json',
				authHeaderKey: authHeaderVal,
			},
			json=self._body,
		)
		CheckResp.CheckRespErr(req)

		return req

	def CliRun(self, auth: _AuthType) -> None:
		self.MakeRequest(auth)

	@staticmethod
	def _AddOpArgParsers(opArgParser: _ArgParserType) -> None:
		opArgParser.add_argument(
			'--dest',  type=str, required=True,
			help='destination file path in the repo',
		)
		opArgParser.add_argument(
			'--commit-msg', type=str, required=True,
			help='Commit message',
		)
		opArgParser.add_argument(
			'--file', type=str, required=True,
			help='Path of the file to upload',
		)
		opArgParser.add_argument(
			'--branch', type=str, required=True,
			help='Branch name',
		)
		opArgParser.add_argument(
			'--sha', type=str, required=False,
			help='SHA of the file to update'
				' (only required when updating a file)',
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

		# read in file
		with open(args.file, 'rb') as f:
			content = f.read()

		# convert to base64
		contentB64 = base64.b64encode(content).decode('utf-8')

		return cls(
			owner=owner,
			repoName=repoName,
			destPath=args.dest,
			commitMsg=args.commit_msg,
			contentBase64=contentB64,
			branch=args.branch,
			sha=args.sha,
		)
