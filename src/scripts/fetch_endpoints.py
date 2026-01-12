import json
import urllib.request
import urllib.error

BASE = 'http://127.0.0.1:6868'

def post_json(path, data):
    url = BASE + path
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req, timeout=10) as r:
        return r.getcode(), r.read().decode()


def get_json(path, token=None):
    url = BASE + path
    headers = {}
    if token:
        headers['Authorization'] = 'Bearer ' + token
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.getcode(), r.read().decode()
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return e.code, body
    except Exception as e:
        return None, str(e)


def pretty_print(title, code, body):
    print('='*60)
    print(title)
    print('STATUS:', code)
    try:
        parsed = json.loads(body)
        print(json.dumps(parsed, ensure_ascii=False, indent=2))
    except Exception:
        print(body)


if __name__ == '__main__':
    # login
    code, body = post_json('/api/auth/login', {'user_name':'kc1015','password':'58997'})
    if code != 200:
        pretty_print('LOGIN FAILED', code, body)
        raise SystemExit(1)
    resp = json.loads(body)
    token = resp.get('token')
    pretty_print('LOGIN RESPONSE', code, body)

    endpoints = [
        '/api/categories/',
        '/api/products/',
        '/api/owner/customers/',
        '/api/owner/sellers/',
        '/api/employee/customers/'
    ]

    for ep in endpoints:
        code, body = get_json(ep, token=token)
        pretty_print(ep, code, body)
