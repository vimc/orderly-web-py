from orderlyweb_api.orderly_web_api import OrderlyWebAPI
from orderlyweb_api.orderly_web_response_error import OrderlyWebResponseError
import pytest
import requests
import time
from datetime import datetime, timedelta


def get_montagu_token():
    url = 'http://localhost:8080/v1/authenticate/'
    data = 'grant_type=client_credentials'
    auth = ('test.user@example.com', 'password')
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=data, auth=auth,
                             headers=headers)
    if response.status_code != 200:
        msg = 'Unexpected status code: {}. Unable to authenticate.'
        raise Exception(msg.format(response.status_code))
    return response.json()['access_token']


base_url = 'http://localhost:8888'
montagu_token = get_montagu_token()


def test_init():
    api = OrderlyWebAPI(base_url, montagu_token)
    assert len(api.token) > 0


def test_error_on_incorrect_credentials():
    with pytest.raises(OrderlyWebResponseError) as ex:
        OrderlyWebAPI(base_url, 'bad token')
    assert 'Unexpected status code: 401. Unable to authenticate' \
           in str(ex)


def test_run_report():
    api = OrderlyWebAPI(base_url, montagu_token)
    key = api.run_report('minimal', {})
    assert len(key) > 0


def test_error_on_post():
    api = OrderlyWebAPI(base_url, montagu_token)
    with pytest.raises(OrderlyWebResponseError) as ex:
        api.post("nonexistent-path", '')
    assert 'Unexpected status code: 404' in str(ex)


def test_report_status():
    api = OrderlyWebAPI(base_url, montagu_token)
    key = api.run_report('minimal', {})
    result = api.report_status(key)
    assert result.status == "queued"
    assert result.version is None
    assert len(result.output["stderr"]) == 0
    assert len(result.output["stdout"]) > 0
    assert not result.success
    assert not result.fail
    assert not result.finished


def test_run_report_to_completion():
    api = OrderlyWebAPI(base_url, montagu_token)
    key = api.run_report('minimal', {})
    finished = False
    timeout = datetime.now() + timedelta(minutes=1)
    while not finished and datetime.now() < timeout:
        time.sleep(0.5)
        result = api.report_status(key)
        finished = result.finished
    assert result.status == "success"
    assert result.finished
    assert result.success
    assert not result.fail
    assert len(result.version) > 0
    assert result.output is None
