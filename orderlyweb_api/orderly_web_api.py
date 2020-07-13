from orderlyweb_api.report_status_result import ReportStatusResult
from orderlyweb_api.orderly_web_response_error import OrderlyWebResponseError
import requests


class OrderlyWebAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url
        auth_url = self.build_url('login')
        headers = {'Authorization': 'token {}'.format(token)}
        response = requests.post(auth_url, headers=headers)
        if response.status_code != 200:
            msg = 'Unexpected status code: {}. Unable to authenticate.'
            raise OrderlyWebResponseError(msg.format(response.status_code),
                                          response=response)
        self.token = response.json()['access_token']

    def run_report(self, report, params):
        result = self.post('reports/{}/run'.format(report), str(params))
        return result['key']

    def report_status(self, key):
        data = self.get('reports/{}/status'.format(key))
        return ReportStatusResult(data)

    def post(self, route, data):
        headers = self.headers()
        url = self.build_url(route)
        response = requests.post(url, data=data, headers=headers)
        return self.handle_response(response)

    def get(self, route):
        headers = self.headers()
        url = self.build_url(route)
        response = requests.get(url, headers=headers)
        return self.handle_response(response)

    def headers(self):
        return {'Authorization': 'Bearer {}'.format(self.token)}

    def build_url(self, route):
        return '{}/api/v1/{}/'.format(self.base_url, route)

    @staticmethod
    def handle_response(response):
        if response.status_code != 200:
            msg = 'Unexpected status code: {}'
            raise OrderlyWebResponseError(msg.format(response.status_code),
                                          response=response)
        return response.json()['data']
