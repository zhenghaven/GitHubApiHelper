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
	_RespType,
)


class GetByTag(ApiRunner):
	# https://docs.github.com/en/rest/releases/releases#get-a-release-by-tag-name

	URL_BASE = 'https://{api_host}/repos/{owner}/{repo}/releases/tags/{tag}'

	def __init__(
		self,
		owner: str,
		repoName: str,
		tag: str,
		hostGetter: HostGetter = DefaultApiHost(),
	) -> None:
		super(GetByTag, self).__init__()

		self._url = self.URL_BASE.format(
			api_host=hostGetter.GetHost(),
			owner=owner,
			repo=repoName,
			tag=tag,
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
