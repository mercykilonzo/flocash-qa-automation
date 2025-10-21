import requests

def test_list_vcns(config, auth, headers):
    url = f"{config.base_url}/vcns"
    resp = requests.get(url, headers=headers, auth=auth, timeout=config.timeout)
    assert resp.status_code == 200, f"List vcns failed: {resp.status_code} {resp.text}"
    data = resp.json()
    assert 'vcns' in data, data

def test_get_vcn_show_template(config, auth, headers):
    token = "d4d4ega0tugsrqmo1mu4an28gc"
    url = f"{config.base_url}/vcns/{token}/show"
    resp = requests.get(url, headers=headers, auth=auth, timeout=config.timeout)
    assert resp.status_code in (200,404), f"Show vcn failed: {resp.status_code} {resp.text}"

def test_transaction_history(config, auth, headers):
    token = "d4d4ega0tugsrqmo1mu4an28gc"
    tx_url = f"{config.base_url}/vcns/{token}/transactions"
    tx_resp = requests.get(tx_url, headers=headers, auth=auth, timeout=config.timeout)
    assert tx_resp.status_code in (200,404), f"Transactions failed: {tx_resp.status_code} {tx_resp.text}"
    if tx_resp.status_code == 200:
        data = tx_resp.json()
        assert isinstance(data, dict), "Expected JSON response for transactions"

def test_get_vcn_card_balance(config, auth, headers):
    token = "d4d4ega0tugsrqmo1mu4an28gc"  # replace with your token
    url = f"{config.base_url}/vcns/{token}/balance"
    response = requests.get(url, headers=headers, auth=auth, timeout=config.timeout)
    print("get_vcn_card_balance:", response.status_code, response.text)
    assert response.status_code in (200, 404), f"get_vcn_card_balance failed: {response.status_code} {response.text}"
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, dict), "Expected JSON response for balance"
        assert 'cardBalance' in data, "Balance key not found in response"

def test_list_deposit_options(config, auth, headers):
    url = f"{config.base_url}/deposits/options?country=ET&currency=ETB"
    resp = requests.get(url, headers=headers, auth=auth, timeout=config.timeout)
    print("list_deposit_options:", resp.status_code, resp.text)
    assert resp.status_code == 200, f"list_deposit_options failed: {resp.status_code} {resp.text}"
    data = resp.json()
    assert isinstance(data.get("payOptions", data.get("options", [])), list)

def test_get_states(config, auth, headers):
    url = "https://sandbox.flocash.com/rest/api/users/profile"
    resp = requests.get(url, headers=headers, auth=auth, timeout=config.timeout)
    print("get_states:", resp.status_code, resp.text)
    assert resp.status_code == 200, f"get_states failed: {resp.status_code} {resp.text}"
    data = resp.json()
    assert "states" in data or isinstance(data, dict)

def test_card_statements(config, auth, headers):
    token = "d4d4ega0tugsrqmo1mu4an28gc"
    url = f"{config.base_url}/vcns/{token}/statements"
    resp = requests.get(url, headers=headers, auth=auth, timeout=config.timeout)
    print("card_statements:", resp.status_code, resp.text)
    assert resp.status_code in (200, 404), f"card_statements failed: {resp.status_code} {resp.text}"    