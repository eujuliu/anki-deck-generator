import requests


def fetch(
    url, timeout=5, headers: dict = {}
) -> dict | requests.exceptions.RequestException:
    try:
        response = requests.get(url, timeout=timeout, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        return err
