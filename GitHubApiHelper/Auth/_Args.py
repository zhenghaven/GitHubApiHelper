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

from ..Utils import LogEnvVars
from . import AccessToken
from . import AppPrivateKey


_AuthTypes = Union[AccessToken.AccessToken, None]


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
	LogEnvVars.LogEnvVars()
	if args.auth_token:
		token = os.environ['GITHUB_TOKEN']
		return AccessToken.AccessToken(token=token)
	elif args.auth_gh_app:
		privKey = os.environ['GITHUB_APP_PRIVATE_KEY']
		appId = os.environ['GITHUB_APP_ID']

		installId = os.environ.get('GITHUB_APP_INSTALLATION_ID', None)
		repo = os.environ.get('GITHUB_APP_REPO', None)
		if installId is None and repo is None:
			raise ValueError(
				'Either GITHUB_APP_INSTALLATION_ID or GITHUB_APP_REPO must be set'
			)
		elif installId is not None:
			return AppPrivateKey.AppPrivateKeyByInstallId(
				privKey=privKey,
				appId=appId,
				installId=installId,
			)
		elif repo is not None:
			owner, repoName = repo.split('/', maxsplit=1)
			return AppPrivateKey.AppPrivateKeyByRepo(
				privKey=privKey,
				appId=appId,
				owner=owner,
				repoName=repoName,
			)

	raise ValueError('No valid authentication method is specified')
