#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


import argparse

from . import ApiContents
from . import ApiRunner
from . import ApiUser
from . import GhRelease
from ._Types import _SubParserAdderType


OPERATION_CLASS_MAP = {
	'api_content_put': {
		'cls': ApiContents.CreateOrUpdate,
		'help': 'API:Contents: Create or update file contents',
	},
	'api_user_get': {
		'cls': ApiUser.GetLogin,
		'help': 'API:User: Get user login',
	},
	'gh_release_dl': {
		'cls': GhRelease.DownloadAsset,
		'help': 'GitHub:Release: Download release asset',
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
