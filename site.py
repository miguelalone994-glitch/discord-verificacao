from flask import Flask, request
import requests
import os

app = Flask(__name__)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
BOT_TOKEN = os.getenv("BOT_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
ROLE_ID = os.getenv("ROLE_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")

@app.route("/")
def home():
    return "Servidor de verificação online"

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Código não encontrado"

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    token = requests.post(
        "https://discord.com/api/oauth2/token",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    ).json()

    if "access_token" not in token:
        return "Erro ao obter token"

    user = requests.get(
        "https://discord.com/api/users/@me",
        headers={
            "Authorization": f"Bearer {token['access_token']}"
        }
    ).json()

    user_id = user["id"]

    role_url = f"https://discord.com/api/v10/guilds/{GUILD_ID}/members/{user_id}/roles/{ROLE_ID}"

    r = requests.put(
        role_url,
        headers={"Authorization": f"Bot {BOT_TOKEN}"}
    )

    if r.status_code == 204:
        return "✅ Verificado com sucesso!"
    else:
        return f"Erro ao dar cargo ({r.status_code})"

app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
