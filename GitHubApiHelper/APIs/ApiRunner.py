#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


from ._Types import (
	_AuthType,
	_ArgsType,
	_ArgParserType,
	_RespType,
)


class ApiRunner(object):
	def __init__(self) -> None:
		super(ApiRunner, self).__init__()

	def MakeRequest(self, auth: _AuthType) -> _RespType:
		raise NotImplementedError('MakeRequest() is not implemented')

	def CliRun(self, auth: _AuthType) -> None:
		raise NotImplementedError('CliRun() is not implemented')

	@staticmethod
	def _AddOpArgParsers(opArgParser: _ArgParserType) -> None:
		raise NotImplementedError('AddOpArgParsers() is not implemented')

	@classmethod
	def FromArgs(cls, args: _ArgsType) -> 'ApiRunner':
		raise NotImplementedError('FromArgs() is not implemented')
