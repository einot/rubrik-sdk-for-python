# Copyright 2024 Rubrik, Inc.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.

import os
import pprint
import requests
from requests.exceptions import RequestException

class RscClient:
    def __init__(self, domain=None, client_id=None, client_secret=None):
        self._pp = pprint.PrettyPrinter(indent=4)

        self._domain = self._get_cred('RSC_DOMAIN', domain)
        self._client_id =\
            self._get_cred('RSC_CLIENT_ID', client_id)
        self._client_secret =\
            self._get_cred('RSC_CLIENT_SECRET', client_secret)

        if not all([self._domain, self._client_id, self._client_secret]):
            raise Exception('Required credentials are missing! Please pass in client id, client secret, and domain, either directly or through the OS environment.')

        try:
            access_token =\
                self._get_access_token(
                    self._client_id,
                    self._client_secret,
                    self._domain,
                )
            self._headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
        except (RequestException, OSError, Exception) as err:
            raise err

        finally:
            # Remove sensitive data
            del self._client_id
            del self._client_secret

    @staticmethod
    def _get_cred(env_key, override=None):
        return override if override else os.environ.get(env_key)

    @staticmethod
    def _get_access_token(client_id, client_secret, domain):
        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "client_id": client_id,
            "client_secret": client_secret
        }

        response =\
            requests.post(
                f"https://{domain}/api/client_token",
                headers=headers,
                json=data,
            )
        response.raise_for_status()  # Raises an exception for HTTP errors

        json_response = response.json()
        access_token = json_response.get("access_token")

        if not access_token:
            raise ValueError("Could not retrieve access token")

        return access_token
