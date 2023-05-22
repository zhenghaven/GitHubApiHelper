#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


import logging
import os


def LogEnvVars() ->None:
	logger = logging.getLogger(__name__ + '.' + LogEnvVars.__name__)
	envVars = [ k for k in os.environ.keys() ]
	logger.debug(
		f'Current environment variables: {envVars}'
	)
