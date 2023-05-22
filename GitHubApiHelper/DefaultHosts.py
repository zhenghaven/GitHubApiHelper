#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


class HostGetter(object):
	def __init__(self) -> None:
		super(HostGetter, self).__init__()

	def GetHost(self) -> str:
		raise NotImplementedError('GetHost() is not implemented')


class DefaultApiHost(HostGetter):
	def __init__(self) -> None:
		super(DefaultApiHost, self).__init__()

	def GetHost(self) -> str:
		return 'api.github.com'


class DefaultGhHost(HostGetter):
	def __init__(self) -> None:
		super(DefaultGhHost, self).__init__()

	def GetHost(self) -> str:
		return 'github.com'
