#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


import base64
import os
import nacl.encoding
import nacl.public
import requests

from ..Auth import GhAppPrivateKey
from ..DefaultHosts import DefaultApiHost, HostGetter
from ..Utils import CheckResp, LogEnvVars
from .ApiRunner import ApiRunner
from ._Types import (
	_AuthType,
	_ArgsType,
	_ArgParserType,
	_RespType,
)


class GetRepoPubKey(ApiRunner):
	# https://docs.github.com/en/rest/actions/secrets#get-a-repository-public-key

	URL_BASE = 'https://{api_host}/repos/{owner}/{repo}/actions/secrets/public-key'

	def __init__(
		self,
		owner: str,
		repoName: str,
		hostGetter: HostGetter = DefaultApiHost(),
	) -> None:
		super(GetRepoPubKey, self).__init__()

		self._url = self.URL_BASE.format(
			api_host=hostGetter.GetHost(),
			owner=owner,
			repo=repoName,
		)

	def MakeRequest(self, auth: _AuthType) -> _RespType:
		authHeaderKey, authHeaderVal = auth.GetHeader()

		req = requests.get(
			url=self._url,
			headers={
				'Accept': 'application/vnd.github+json',
				authHeaderKey: authHeaderVal,
			},
		)
		CheckResp.CheckRespErr(req)

		return req


class SetRepoSecret(ApiRunner):
	# https://docs.github.com/en/rest/actions/secrets#create-or-update-a-repository-secret

	URL_BASE = 'https://{api_host}/repos/{owner}/{repo}/actions/secrets/{secret_name}'

	def __init__(
		self,
		owner: str,
		repoName: str,
		repoPubKey: str,
		repoPubKeyID: str,
		secretName: str,
		secretValue: str,
		hostGetter: HostGetter = DefaultApiHost(),
	) -> None:
		super(SetRepoSecret, self).__init__()

		self._url = self.URL_BASE.format(
			api_host=hostGetter.GetHost(),
			owner=owner,
			repo=repoName,
			secret_name=secretName,
		)

		self._repoPubKey = repoPubKey
		self._repoPubKeyID = repoPubKeyID
		self._secretValue = secretValue

	def _EncryptSecret(self) -> str:
		pubKey = nacl.public.PublicKey(
			self._repoPubKey.encode("utf-8"),
			nacl.encoding.Base64Encoder()
		)
		sealedBox = nacl.public.SealedBox(pubKey)
		encrypted = sealedBox.encrypt(self._secretValue.encode("utf-8"))
		return base64.b64encode(encrypted).decode("utf-8")

	def _GenPayload(self) -> dict:
		return {
			'encrypted_value': self._EncryptSecret(),
			'key_id': self._repoPubKeyID,
		}

	def MakeRequest(self, auth: _AuthType) -> _RespType:
		authHeaderKey, authHeaderVal = auth.GetHeader()

		req = requests.put(
			url=self._url,
			headers={
				'Accept': 'application/vnd.github+json',
				authHeaderKey: authHeaderVal,
			},
			json=self._GenPayload(),
		)
		CheckResp.CheckRespErr(req)

		return req


class SetRepoSecretFromGhApp(ApiRunner):

	def __init__(
		self,
		owner: str,
		repoName: str,
		secretName: str,
		hostGetter: HostGetter = DefaultApiHost(),
	) -> None:
		super(SetRepoSecretFromGhApp, self).__init__()

		self._owner = owner
		self._repoName = repoName
		self._secretName = secretName
		self._hostGetter = hostGetter

	def CliRun(self, auth: _AuthType) -> None:

		pubKeyGetter = GetRepoPubKey(
			owner=self._owner,
			repoName=self._repoName,
			hostGetter=self._hostGetter,
		)
		pubKeyRespJson = pubKeyGetter.MakeRequest(auth).json()
		pubKey = pubKeyRespJson['key']
		pubKeyID = pubKeyRespJson['key_id']

		appKeyGetter = GhAppPrivateKey.FromEnvVars()
		token = appKeyGetter.GetToken()

		secretSetter = SetRepoSecret(
			owner=self._owner,
			repoName=self._repoName,
			repoPubKey=pubKey,
			repoPubKeyID=pubKeyID,
			secretName=self._secretName,
			secretValue=token,
			hostGetter=self._hostGetter,
		)
		secretSetter.MakeRequest(auth)

	@staticmethod
	def _AddOpArgParsers(opArgParser: _ArgParserType) -> None:
		opArgParser.add_argument(
			'--secret', type=str, required=True,
			help='The name of the secret to create or update.',
		)

	@classmethod
	def FromArgs(cls, args: _ArgsType) -> ApiRunner:
		LogEnvVars.LogEnvVars()
		repo = os.environ['GITHUB_REPOSITORY']
		owner, repoName = repo.split('/', maxsplit=1)
		return cls(
			owner=owner,
			repoName=repoName,
			secretName=args.secret,
		)
