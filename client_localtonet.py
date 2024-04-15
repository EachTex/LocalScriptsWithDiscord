import requests, random, json, time

apps = [
    "App A",
    "App B",
    "App C"
]
auth_pin = random.randint(10000, 99999)

data = {
    "products": apps,
    "auth_pin": auth_pin
}
connect_data = json.dumps(data)

req = requests.post(
    url = f"https://127.0.0.1:12958",
    data = connect_data
)
print(f"Auth PIN: {auth_pin}")
print(f"Connect ID: {req.json()['connect_id']}")

detail = {
    "auth_pin": int(auth_pin),
    "connect_id": int(req.json()['connect_id'])
}
details = json.dumps(detail)

print(f"Waiting for connection...")

_connected = False
while True:
    res = requests.post(
        url = f"https://127.0.0.1:12958status",
        data = details
    )
    content = res.json()
    if content['status'] == 404:
        print("Internal Server Error Occurred.")
        exit()

    elif content['status'] == 1 and _connected == False:
        _connected = True
        print(f"Connected with {content['user_id']}.")
        time.sleep(3)

    elif content['status'] == 1 and _connected == True:
        time.sleep(3)

    elif content['status'] == 2:
        products = content['products']
        break

    else:
        time.sleep(3)

print(f"Choosed products: {products}")