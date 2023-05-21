#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


import requests

from ..DefaultHosts import DefaultApiHost, HostGetter
from ..Utils import CheckResp
from .ApiRunner import ApiRunner
from ._Types import (
	_AuthType,
	_ArgsType,
	_ArgParserType,
	_RespType,
)


class Get(ApiRunner):
	# https://docs.github.com/en/rest/users/users#get-the-authenticated-user

	URL_BASE = 'https://{api_host}/user'

	def __init__(
		self,
		hostGetter: HostGetter = DefaultApiHost(),
	) -> None:
		super(Get, self).__init__()

		self._url = self.URL_BASE.format(
			api_host=hostGetter.GetHost(),
		)

	def MakeRequest(self, auth: _AuthType) -> _RespType:
		authHeaderKey, authHeaderVal = auth.GetHeader()

		req = requests.get(
			url=self._url,
			headers={
				'Accept': 'application/vnd.github+json',
				authHeaderKey: authHeaderVal,
			},
		)
		CheckResp.CheckRespErr(req)

		return req


class GetLogin(Get):

	def __init__(
		self,
		hostGetter: HostGetter = DefaultApiHost(),
	) -> None:
		super(GetLogin, self).__init__(hostGetter)

	def CliRun(self, auth: _AuthType) -> None:
		resp = self.MakeRequest(auth)
		CheckResp.LogHeaders(resp)
		userJson = resp.json()
		print(userJson['login'])

	@staticmethod
	def _AddOpArgParsers(opArgParser: _ArgParserType) -> None:
		pass

	@classmethod
	def FromArgs(cls, args: _ArgsType) -> ApiRunner:
		return cls()
