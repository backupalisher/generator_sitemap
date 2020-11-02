import requests


def check_url(url):
    session = requests.Session()
    request = session.get(url=url)
    if request.status_code == 200:
        return True
    else:
        return False
