from orderlyweb_api.orderly_web_api import OrderlyWebAPI
from orderlyweb_api.orderly_web_response_error import OrderlyWebResponseError
import requests_mock
import pytest

base_url = 'http://test'
api_base_url = base_url + "/api/v1/"


def test_init():
    with requests_mock.mock() as m:
        m.post("{}login/".format(api_base_url),
               text='{"access_token": "fake_token"}')

        api = OrderlyWebAPI(base_url, "fake_montagu_token")
        assert api.token == "fake_token"

        request = m.request_history[0]
        assert request.headers["Authorization"] == "token fake_montagu_token"


def test_init_error():
    with requests_mock.mock() as m:
        m.post("{}login/".format(api_base_url), status_code=500)

        with pytest.raises(OrderlyWebResponseError) as ex:
            OrderlyWebAPI(base_url, "fake_montagu_token")
        assert 'Unexpected status code: 500. Unable to authenticate' \
               in str(ex)
        assert ex.value.response.status_code == 500


def test_run_report():
    params = {"p1": "v1", "p2": 2}
    api = get_test_api()
    with requests_mock.mock() as m:
        m.post("{}reports/test-report/run/".format(api_base_url),
               text='{"data": {"key": "test-key"}}')

        key = api.run_report("test-report", params)
        assert key == "test-key"

        request = m.request_history[0]
        assert request.body == "{'p1': 'v1', 'p2': 2}"


def test_run_report_error():
    params = {}
    api = get_test_api()
    with requests_mock.mock() as m:
        m.post("{}reports/test-report/run/".format(api_base_url),
               status_code=403)
        with pytest.raises(OrderlyWebResponseError) as ex:
            api.run_report("test-report", params)
        assert 'Unexpected status code: 403' in str(ex)
        assert ex.value.response.status_code == 403


def test_report_status():
    api = get_test_api()
    with requests_mock.mock() as m:
        m.get("{}reports/test-key/status/".format(api_base_url),
              text='{"data": {"status": "success", "version": "v1", '
                   '"output": {}}}')
        result = api.report_status("test-key")
        assert result.status == "success"
        assert result.success
        assert result.version == "v1"
        assert result.output == {}


def test_report_status_error():
    api = get_test_api()
    with requests_mock.mock() as m:
        m.get("{}reports/test-key/status/".format(api_base_url),
              status_code=500)
        with pytest.raises(OrderlyWebResponseError) as ex:
            api.report_status("test-key")
        assert 'Unexpected status code: 500' in str(ex)
        assert ex.value.response.status_code == 500


def get_test_api():
    with requests_mock.mock() as m:
        m.post("{}login/".format(api_base_url),
               text='{"access_token": "fake_token"}')

        return OrderlyWebAPI(base_url, "fake_montagu_token")
