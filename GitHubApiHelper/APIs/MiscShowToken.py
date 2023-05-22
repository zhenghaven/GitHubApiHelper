#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


from .ApiRunner import ApiRunner
from ._Types import (
	_AuthType,
	_ArgsType,
	_ArgParserType,
)


class ShowToken(ApiRunner):

	def __init__(self) -> None:
		super(ShowToken, self).__init__()

	def CliRun(self, auth: _AuthType) -> None:
		print(auth.GetToken())

	@staticmethod
	def _AddOpArgParsers(opArgParser: _ArgParserType) -> None:
		pass

	@classmethod
	def FromArgs(cls, args: _ArgsType) -> ApiRunner:
		return cls()
