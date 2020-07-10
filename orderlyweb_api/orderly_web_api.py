import requests


class OrderlyWebAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url
        auth_url = self.build_url('login')
        headers = {'Authorization': 'token {}'.format(token)}
        response = requests.post(auth_url, headers=headers)
        if response.status_code != 200:
            msg = 'Unexpected status code: {}. Unable to authenticate.'
            raise Exception(msg.format(response.status_code))
        self.token = response.json()['access_token']

    def run_report(self, report, params):
        result = self.post('reports/{}/run'.format(report), str(params))
        return result['key']

    def post(self, route, data):
        headers = {'Authorization': 'Bearer {}'.format(self.token)}
        url = self.build_url(route)
        response = requests.post(url, data=data, headers=headers)
        if response.status_code != 200:
            msg = 'Unexpected status code: {}'
            raise Exception(msg.format(response.status_code))
        return response.json()['data']

    def build_url(self, route):
        return '{}/api/v1/{}/'.format(self.base_url, route)
