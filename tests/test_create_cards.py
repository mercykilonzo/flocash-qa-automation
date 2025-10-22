import requests

def test_create_vcn(config, auth, headers):
    url = f"{config.base_url}/vcns"
    response = requests.post(url, headers=headers, auth=auth, timeout=config.timeout)
    assert response.status_code in (200,201), f"Create VCN failed: {response.status_code} {response.text}"
    data = response.json()
    print("VCN Create Resonse:", data)
    assert 'vcn' in data, data
    token = data['vcn'].get('token') or data['vcn'].get('id')
    print("Created VCN Token:", token)


def test_topup_vcn_card_load(config, auth, headers, vcn_token):
    url = f"{config.base_url}/vcns/{vcn_token}/load"
    payload = {
        "load": {"amount": 10000, "currency": "ETB", "remark": "test"},
        "payOption": {"id": 123},
        "payer": {"country": "ET", "firstName": "Shabiha", "lastName": "Dennis", "mobile": "99999999", "email": "dennis@gmail.com"},
        "cardInfo": {"cardHolder": "Dennis Shabiha", "cardNumber": "4005555555000009", "expireMonth": "05", "expireYear": "25", "cvv": "100"}
    }
    response = requests.post(url, json=payload, headers=headers, auth=auth, timeout=config.timeout)
    assert response.status_code in (200,201), f"Topup VCN (card) failed: {response.status_code} {response.text}"
    data = response.json()
    assert 'order' in data or 'status' in data, data


def test_topup_vcn_mobile_load(config, auth, headers, vcn_token):
    url = f"{config.base_url}/vcns/{vcn_token}/load"
    payload = {
        "load": {"amount": 10, "currency": "ETB", "remark": "test"},
        "payOption": {"id": 20},
        "payer": {
            "country": "ET",
            "firstName": "Shabiha",
            "lastName": "Dennis",
            "mobile": "99999999",
            "email": "dennis@gmail.com"
        }
    }
    response = requests.post(url, json=payload, headers=headers, auth=auth, timeout=config.timeout)
    print("Mobile load response:", response.text)
    assert response.status_code in (200, 201, 400), f"Mobile load failed: {response.status_code} {response.text}"


def test_unload_fund(config, auth, headers, vcn_token):
    url = f"{config.base_url}/vcns/{vcn_token}/unload"
    payload = {
        "unload": {
            "amount": 1,
            "currency": "USD",
            "remark": "test unload",
            "type": "BANK",
            "accountId": "160087771"
        }
  }
    response = requests.post(url, json=payload, headers=headers, auth=auth, timeout=config.timeout)
    print("unload_fund:", response.status_code, response.text)
    assert response.status_code in (200,201,400), f"unload_fund failed: {response.status_code} {response.text}"
    if response.status_code in (200,201):
        assert isinstance(response.json(), dict)


def test_create_bank_wallet(config, auth, headers):
    url = "https://sandbox.flocash.com/rest/api/users/banks"
    payload = {
        "bank": {
            "bankName" : "Equity Bank API",
		    "accountNumber" : "0151016900116",
		    "accountHolder" : "Shabiha Assyrian",
		    "swiftCode" : "ghhhg"
        }
    }
    response = requests.post(url, json=payload, headers=headers, auth=auth, timeout=config.timeout)
    print("create_bank_wallet:", response.status_code, response.text)
    assert response.status_code in (200, 201, 400), f"create_bank_wallet failed: {response.status_code} {response.text}"
    data = response.json()
    assert isinstance(data, dict)

def test_create_mobile_wallet(config, auth, headers):
    url = "https://sandbox.flocash.com/rest/api/users/mobileWallet"
    payload = {
        "mobileWallet": {
            "walletNumber": "015101690216",
            "accountName": "Shabiha",
            "operatorName": "MPESA",
            "paybillNumber": "12343335"
        }
    }
    response = requests.post(url, json=payload, headers=headers, auth=auth, timeout=config.timeout)
    print("create_mobile_wallet:", response.status_code, response.text)
    assert response.status_code in (200,201,400), f"create_mobile_wallet failed: {response.status_code} {response.text}"
    assert isinstance(response.json(), dict)