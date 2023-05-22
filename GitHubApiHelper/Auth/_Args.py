#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


import argparse

from ._Types import _AuthTypes
from . import AccessToken
from . import GhAppPrivateKey


def _AddArgParsers(argParser: argparse.ArgumentParser) -> None:
	authGrp = argParser.add_mutually_exclusive_group(required=True)
	authGrp.add_argument(
		'--auth-token', action='store_true',
		help='Use access token as authentication method'
	)
	authGrp.add_argument(
		'--auth-gh-app', action='store_true',
		help='Use GitHub App\'s private key as authentication method'
	)


def _ProcArgs(args: argparse.Namespace) -> _AuthTypes:
	if args.auth_token:
		return AccessToken.FromEnvVars()
	elif args.auth_gh_app:
		return GhAppPrivateKey.FromEnvVars()

	raise ValueError('No valid authentication method is specified')
