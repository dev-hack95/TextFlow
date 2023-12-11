import os
import requests


def token(request):
    if not "Authorization" in request.headers:
        return None, ({"error": "Missing Authorization Header"}, 401)
    
    token = request.headers['Authorization']

    if not token:
        return None, ({"error": "Missing Credientials"}, 401)
    
    response = requests.post(
        f"http://localhost:8000/v1/validate",
        headers={"Authorization": token}
    )

    if response.status_code == 200:
        print(response.text)
        return response.text, None
    else:
        return None, (response.text, response.status_code)