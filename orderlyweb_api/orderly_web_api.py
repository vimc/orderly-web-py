from orderlyweb_api.result_models import ReportStatusResult, VersionDetails

from orderlyweb_api.orderly_web_response_error import OrderlyWebResponseError
import requests


class OrderlyWebAPI:
    def __init__(self, base_url, auth_provider_token):
        self.base_url = base_url
        auth_url = self.build_url('login')
        headers = {'Authorization': 'token {}'.format(auth_provider_token)}
        response = requests.post(auth_url, headers=headers)
        if response.status_code != 200:
            raise OrderlyWebResponseError(response)
        self.access_token = response.json()['access_token']

    def run_report(self, report, params):
        result = self.post('reports/{}/run'.format(report), str(params))
        return result['key']

    def publish_report(self, name, version):
        url = 'reports/{}/versions/{}/publish'.format(name, version)
        return self.post(url, None)

    def report_status(self, key):
        data = self.get('reports/{}/status'.format(key))
        return ReportStatusResult(data)

    def report_versions(self, name):
        return self.get('reports/{}'.format(name))

    def version_details(self, name, version):
        data = self.get('reports/{}/versions/{}'.format(name, version))
        return VersionDetails(data)

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
        return {'Authorization': 'Bearer {}'.format(self.access_token)}

    def build_url(self, route):
        return '{}/api/v1/{}/'.format(self.base_url, route)

    @staticmethod
    def handle_response(response):
        if response.status_code != 200:
            raise OrderlyWebResponseError(response)
        return response.json()['data']
