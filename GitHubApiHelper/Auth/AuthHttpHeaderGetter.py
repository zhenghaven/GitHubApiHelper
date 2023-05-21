#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


from typing import Tuple


class AuthHttpHeaderGetter(object):
	def __init__(self) -> None:
		super(AuthHttpHeaderGetter, self).__init__()

	def GetHeader() -> Tuple[str, str]:
		raise NotImplementedError('GetHeader() is not implemented')
