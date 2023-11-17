import json, httpx
from . import config


def get_jwt(code):
    url = config.pange_domain + '/client/userinfo'
    token = config.pangea_client_token

    response =  httpx.post(
        url, 
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={'code': code}
    )
    data = response.json()
    assert data["status"] == "Success", "Invalid Token. Please run Login again."
    return data

def get_server_config(token):
    url = config.backend_domain + "/server-config"
    response = httpx.get(url, headers={"Authorization": f"Bearer {token}"})
    return json.loads(response.text)

def get_private_keys(token):
    url = config.backend_domain + "/private-keys"
    response = httpx.get(url, headers={"Authorization": f"Bearer {token}"})
    return response.json()

def store_server_configuration(server_configuration):
    pass

def store_ssh_key(secret):
    pass