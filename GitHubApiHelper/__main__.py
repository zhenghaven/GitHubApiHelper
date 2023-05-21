#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


import argparse

from .Auth import _Args as AuthArgs
from .APIs import _Args as ApiArgs
from . import _Meta


def main() -> None:
	argParser = argparse.ArgumentParser(
		description=_Meta.PKG_DESCRIPTION,
	)
	AuthArgs._AddArgParsers(argParser=argParser)
	opArgParser = argParser.add_subparsers(
		title='Operation to perform',
		dest='operation',
	)
	ApiArgs._AddOpArgParsers(opArgParser=opArgParser)
	args = argParser.parse_args()
	authMethod = AuthArgs._ProcArgs(args=args)

	apiRunner = ApiArgs._ProcArgs(args=args)

	apiRunner.CliRun(auth=authMethod)


if __name__ == '__main__':
	main()
