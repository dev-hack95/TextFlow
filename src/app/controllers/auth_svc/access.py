import os
import requests

def login(request):
    auth = request.authorization
    if not auth:
        return None, ("Missing Credentials", 401)

    response = requests.post(
        f"http://localhost:8000/v1/login?email={auth.username}&password={auth.password}"
    )

    if response.status_code == 200:
        return  response.text, None
    else:
        return None, (response.text, f"Authentication failed with code {response.status_code}", 503)