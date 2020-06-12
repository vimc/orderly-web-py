from src.orderly_web_api import OrderlyWebAPI
import pytest
import requests


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
    with pytest.raises(Exception) as ex:
        OrderlyWebAPI(base_url, 'bad token')
    assert 'Unexpected status code: 401. Unable to authenticate' \
           in str(ex)


def test_run_report():
    api = OrderlyWebAPI(base_url, montagu_token)
    key = api.run_report('minimal', {})
    assert len(key) > 0


def test_error_on_post():
    api = OrderlyWebAPI(base_url, montagu_token)
    with pytest.raises(Exception) as ex:
        api.post("nonexistent-path", '')
    assert 'Unexpected status code: 404' in str(ex)
