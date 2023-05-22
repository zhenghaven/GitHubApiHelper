#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


import os
import requests
import time
import jwt

from cryptography.hazmat.primitives import serialization
from typing import Tuple, Union

from ..DefaultHosts import DefaultApiHost, HostGetter
from ..Utils import CheckResp, LogEnvVars

from . import AccessTokenGetter
from . import AuthHttpHeaderGetter


class AppPrivateKey(object):

	def __init__(
		self,
		privKey: Union[bytes, str, os.PathLike],
		appId: str,
		hostGetter: HostGetter = DefaultApiHost(),
	) -> None:

		if os.path.isfile(privKey):
			with open(privKey, 'rb') as f:
				self._privKey = f.read()
		else:
			self._privKey = privKey

		if isinstance(self._privKey, str):
			self._privKey = self._privKey.encode('utf-8')

		if isinstance(self._privKey, bytes) and self._privKey.startswith(b'-----BEGIN'):
			self._privKey = serialization.load_pem_private_key(
				self._privKey,
				password=None,
			)
		else:
			self._privKey = serialization.load_der_private_key(
				self._privKey,
				password=None,
			)

		self._appId = appId
		self._hostGetter = hostGetter

	def _GenPayload(self) -> dict:
		return {
			# Issued at time
			'iat': int(time.time()),
			# JWT expiration time (2 minutes maximum)
			'exp': int(time.time()) + 120,
			# GitHub App's identifier
			'iss': self._appId,
		}

	def _GenEncoded(self) -> str:
		return jwt.encode(
			self._GenPayload(),
			self._privKey,
			algorithm='RS256',
		)

	def GetInstallIdByRepo(
		self,
		owner: str,
		repoName: str,
	) -> int:
		# https://docs.github.com/en/rest/apps/apps#get-a-repository-installation-for-the-authenticated-app

		URL_BASE = 'https://{api_host}/repos/{owner}/{repo}/installation'

		url = URL_BASE.format(
			api_host=self._hostGetter.GetHost(),
			owner=owner,
			repo=repoName,
		)

		resp = requests.get(
			url=url,
			headers={
				'Accept': 'application/vnd.github+json',
				'Authorization': f'Bearer {self._GenEncoded()}',
			},
		)
		CheckResp.CheckRespErr(resp)

		return resp.json()['id']

	def GetInstallToken(self, installId: int) -> str:
		# https://docs.github.com/en/rest/apps/apps#create-an-installation-access-token-for-an-app

		URL_BASE = 'https://{api_host}/app/installations/{install_id}/access_tokens'

		url = URL_BASE.format(
			api_host=self._hostGetter.GetHost(),
			install_id=installId,
		)

		resp = requests.post(
			url=url,
			headers={
				'Accept': 'application/vnd.github+json',
				'Authorization': f'Bearer {self._GenEncoded()}',
			},
		)
		CheckResp.CheckRespErr(resp)

		return resp.json()['token']


class AppPrivateKeyByInstallId(
	AccessTokenGetter.AccessTokenGetter,
	AuthHttpHeaderGetter.AuthHttpHeaderGetter
):
	def __init__(
		self,
		privKey: Union[bytes, str, os.PathLike],
		appId: str,
		installId: int,
		hostGetter: HostGetter = DefaultApiHost(),
	) -> None:
		super(AppPrivateKeyByInstallId, self).__init__()

		self._privKey = AppPrivateKey(
			privKey=privKey,
			appId=appId,
			hostGetter=hostGetter,
		)
		self._installId = installId

	def GetToken(self) -> str:
		return self._privKey.GetInstallToken(self._installId)

	def GetHeader(self) -> Tuple[str, str]:
		return ('Authorization', f'Bearer {self.GetToken()}')


class AppPrivateKeyByRepo(
	AppPrivateKeyByInstallId
):
	def __init__(
		self,
		privKey: Union[bytes, str, os.PathLike],
		appId: str,
		owner: str,
		repoName: str,
		hostGetter: HostGetter = DefaultApiHost(),
	) -> None:
		super(AppPrivateKeyByRepo, self).__init__(
			privKey=privKey,
			appId=appId,
			installId=0,
			hostGetter=hostGetter,
		)

		self._owner = owner
		self._repoName = repoName

		self._installId = self._privKey.GetInstallIdByRepo(
			owner=owner,
			repoName=repoName,
		)


def FromEnvVars() -> AppPrivateKeyByInstallId:
	LogEnvVars.LogEnvVars()

	privKey = os.environ['GITHUB_APP_PRIVATE_KEY']
	appId = os.environ['GITHUB_APP_ID']

	installId = os.environ.get('GITHUB_APP_INSTALLATION_ID', None)
	repo = os.environ.get('GITHUB_APP_REPO', None)
	if installId is None and repo is None:
		raise ValueError(
			'Either GITHUB_APP_INSTALLATION_ID or GITHUB_APP_REPO must be set'
		)
	elif installId is not None:
		return AppPrivateKeyByInstallId(
			privKey=privKey,
			appId=appId,
			installId=installId,
		)
	elif repo is not None:
		owner, repoName = repo.split('/', maxsplit=1)
		return AppPrivateKeyByRepo(
			privKey=privKey,
			appId=appId,
			owner=owner,
			repoName=repoName,
		)
