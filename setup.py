#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


from setuptools import setup
from setuptools import find_packages

import GitHubApiHelper._Meta


setup(
	name        = GitHubApiHelper._Meta.PKG_NAME,
	version     = GitHubApiHelper._Meta.__version__,
	packages    = find_packages(where='.', exclude=['main.py']),
	url         = 'https://github.com/zhenghaven/GitHubApiHelper',
	license     = GitHubApiHelper._Meta.PKG_LICENSE,
	author      = GitHubApiHelper._Meta.PKG_AUTHOR,
	description = GitHubApiHelper._Meta.PKG_DESCRIPTION,
	entry_points= {
		'console_scripts': [
			'GitHubApiHelper=GitHubApiHelper.__main__:main',
		]
	},
	install_requires=[
		'requests>=2.30.0',
		'PyJWT>=2.7.0',
		'cryptography>=40.0.2',
		'PyNaCl>=1.5.0',
		'packaging>=23.2',
	],
)
