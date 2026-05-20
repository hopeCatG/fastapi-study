import json
import urllib.error
import urllib.parse
import urllib.request


def post_json(url: str, params: dict) -> dict:
    data = json.dumps(params, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        body = response.read().decode("utf-8")
    return json.loads(body)


def get_json(url: str, params: dict) -> dict:
    full_url = f"{url}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(full_url, timeout=60) as response:
        body = response.read().decode("utf-8")
    return json.loads(body)
