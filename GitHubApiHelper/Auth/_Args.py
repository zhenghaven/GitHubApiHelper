#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


import argparse
import os

from typing import Union

from . import AccessToken


_AuthTypes = Union[AccessToken.AccessToken, None]


def _AddArgParsers(argParser: argparse.ArgumentParser) -> None:
	authGrp = argParser.add_mutually_exclusive_group(required=False)
	authGrp.add_argument(
		'--auth-env',
		type=str, required=False, default='GITHUB_TOKEN',
		help='The name of the environment variable used to retrieve the access token',
	)


def _ProcArgs(args: argparse.Namespace) -> _AuthTypes:
	if args.auth_env is not None:
		token = os.environ.get(args.auth_env)
		if token is not None:
			return AccessToken.AccessToken(token=token)

	raise ValueError('No valid authentication method is specified')
