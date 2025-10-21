import requests
def test_cancel_card(config, auth, headers, vcn_token):
    url = f"https://sandbox.flocash.com/rest/v2/vcns/{vcn_token}/close"
    resp = requests.post(url, headers=headers, auth=auth, timeout=config.timeout)
    print("cancel_card:", resp.status_code, resp.text)
    assert resp.status_code in (200,204,400,404), f"cancel_card failed: {resp.status_code} {resp.text}"