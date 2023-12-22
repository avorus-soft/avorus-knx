import os

import requests


class Api:
    def __init__(self):
        self.token = None
        self.api_url = f'https://{os.environ["API_HOSTNAME"]}:443'

    def login(self):
        auth_data = {
            'username': (None, os.environ['API_SYSTEM_USERNAME']),
            'password': (None, os.environ['API_SYSTEM_PASSWORD'])
        }
        response = requests.request(
            'POST',
            f'{self.api_url}/auth/jwt/login',
            files=auth_data,
            verify=os.environ['API_ROOT_CA'])
        self.token = response.json()['access_token']

    def get(self, path):
        headers = {
            'authorization': f'Bearer {self.token}'
        }
        response = requests.get(
            f'{self.api_url}{path}',
            headers=headers,
            verify=os.environ['API_ROOT_CA'])
        if response.status_code == 401:
            self.login()
            return self.get(path)
        else:
            return response
