import requests


def get_ngrok_url():
    response = requests.get("http://ngrok:4040/api/tunnels")
    tunnels = response.json()["tunnels"]
    for tunnel in tunnels:
        if tunnel["proto"] == "https":
            return tunnel["public_url"]
