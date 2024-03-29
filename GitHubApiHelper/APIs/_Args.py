#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


import argparse

from . import ApiActionsSecrets
from . import ApiContents
from . import ApiReleaseAssets
from . import ApiRunner
from . import ApiTags
from . import ApiUser
from . import GhRelease
from . import MiscShowToken
from ._Types import _SubParserAdderType


OPERATION_CLASS_MAP = {
	'api_actions_secrets_from_gh_app': {
		'cls': ApiActionsSecrets.SetRepoSecretFromGhApp,
		'help': 'API:Actions:Secrets: Set repository secret from GitHub App token',
	},
	'api_content_put': {
		'cls': ApiContents.CreateOrUpdate,
		'help': 'API:Contents: Create or update file contents',
	},
	'api_release_asset_dl': {
		'cls': ApiReleaseAssets.Download,
		'help': 'GitHub:Release:Assets Download release asset',
	},
	'api_tags': {
		'cls': ApiTags.GetTagList,
		'help': 'API:Tags: Get list of tags',
	},
	'api_tags_latest_ver': {
		'cls': ApiTags.GetLatestVer,
		'help': 'API:Tags: Get latest version tag',
	},
	'api_user_get': {
		'cls': ApiUser.GetLogin,
		'help': 'API:User: Get user login',
	},
	'gh_release_dl': {
		'cls': GhRelease.DownloadAsset,
		'help': 'GitHub:Release: Download release asset',
	},
	'misc_show_token': {
		'cls': MiscShowToken.ShowToken,
		'help': 'Misc:ShowToken: Print authentication token to stdout',
	},
}


def _AddOpArgParsers(opArgParser: _SubParserAdderType) -> None:
	for opName, opInfo in OPERATION_CLASS_MAP.items():
		subParser = opArgParser.add_parser(name=opName, help=opInfo['help'])
		cls: ApiRunner.ApiRunner = opInfo['cls']
		cls._AddOpArgParsers(opArgParser=subParser)


def _ProcArgs(args: argparse.Namespace) -> ApiRunner.ApiRunner:
	opInfo = OPERATION_CLASS_MAP[args.operation]
	cls: ApiRunner.ApiRunner = opInfo['cls']
	return cls.FromArgs(args=args)
