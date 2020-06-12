from src.orderly_web_api import OrderlyWebAPI
import pytest
import requests


def getMontaguToken():
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
montagu_token = getMontaguToken()


def test_init():
    api = OrderlyWebAPI(base_url, montagu_token)
    assert len(api.token) > 0


#def test_error_on_incorrect_credentials():
#    with pytest.raises(Exception) as ex:
#        MontaguAPI(base_url, user, 'wrong password')
#    assert 'Exception: Unexpected status code: 401. Unable to authenticate.' \
#           in str(ex)


#def test_diseases():
#    api = MontaguAPI(base_url, user, password)
#    diseases = api.diseases()
#    assert len(diseases) == 1
#    disease = diseases[0]
#    assert disease['id'] == 'YF'
#    assert disease['name'] == 'Yellow Fever'


#def test_error_on_get():
#    api = MontaguAPI(base_url, user, password)
#    with pytest.raises(Exception) as ex:
#        api.get("nonexistent-path")
#    assert 'Exception: Unexpected status code: 404' in str(ex)


