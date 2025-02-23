import requests


def get_ngrok_url(url):
    response = requests.get(f"{url}/api/tunnels")
    tunnels = response.json()["tunnels"]
    for tunnel in tunnels:
        if tunnel["proto"] == "https":
            return tunnel["public_url"]
