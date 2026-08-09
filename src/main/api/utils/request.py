import requests
from src.main.api.config import BASE_URL


def post(endpoint, json=None, token=None, expected_status=200):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.post(url, json=json, headers=headers)

    if expected_status is not None:
        assert response.status_code == expected_status, \
            f"Expected status: {expected_status}, getting: {response.status_code}. Response body: {response.text}"
    return response


def get(endpoint, token=None, expected_status=200):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.get(url, headers=headers)

    if expected_status is not None:
        assert response.status_code == expected_status, \
            f"Expected status: {expected_status}, getting: {response.status_code}. Response body: {response.text}"
    return response


def delete(endpoint, json=None, token=None, expected_status=200):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.delete(url, json=json, headers=headers)

    if expected_status is not None:
        assert response.status_code == expected_status, \
            f"Expected status: {expected_status}, getting: {response.status_code}. Response body: {response.text}"
    return response
