#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


import argparse
import requests

from ..Auth import AuthHttpHeaderGetter


_AuthType = AuthHttpHeaderGetter.AuthHttpHeaderGetter
_ArgsType = argparse.Namespace
_ArgParserType = argparse.ArgumentParser
_RespType = requests.Response


class _SubParserAdderType:
	def add_parser(self, name: str, **kwargs) -> _ArgParserType:
		raise NotImplementedError('add_parser() is not implemented')
