#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


from typing import Tuple
from . import AccessTokenGetter
from . import AuthHttpHeaderGetter


class AccessToken(
	AccessTokenGetter.AccessTokenGetter,
	AuthHttpHeaderGetter.AuthHttpHeaderGetter
):
	def __init__(self, token: str) -> None:
		super(AccessToken, self).__init__()

		self.token = token

	def GetToken(self) -> str:
		return self.token

	def GetHeader(self) -> Tuple[str, str]:
		return ('Authorization', f'Bearer {self.token}')
