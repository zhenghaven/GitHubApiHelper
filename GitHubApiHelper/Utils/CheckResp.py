#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


import logging
import requests


def LogScope(resp: requests.Response) -> None:
	logger = logging.getLogger(__name__ + '.' + LogScope.__name__)
	if 'X-Accepted-OAuth-Scopes' in resp.headers:
		acceptScopes = resp.headers['X-Accepted-OAuth-Scopes']
		logger.info(f'Accepted Scopes: {acceptScopes}')
	if 'X-OAuth-Scopes' in resp.headers:
		recvScope = resp.headers["X-OAuth-Scopes"]
		logger.info(f'Scopes: {recvScope}')


def CheckRespErr(resp: requests.Response) -> None:
	try:
		resp.raise_for_status()
	except requests.exceptions.HTTPError:
		logger = logging.getLogger(__name__ + '.' + CheckRespErr.__name__)
		if 'Content-Type' in resp.headers:
			if resp.headers['Content-Type'].startswith('application/json'):
				logger.error(resp.json())
			if resp.headers['Content-Type'].startswith('text/'):
				logger.error(resp.text)

		LogScope(resp)

		raise
