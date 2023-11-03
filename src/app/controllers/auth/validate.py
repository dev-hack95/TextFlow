import os
import requests
from fastapi import status

def token(request):
    if not "Authorization" in request.headers:
        return None, ({"error": "Missing Authorization Header"}, status.HTTP_401_UNAUTHORIZED)
    
    token = request.headers['Authorization']

    if not token:
        return None, ({"error": "Missing Credientials"}, status.HTTP_401_UNAUTHORIZED)
    
    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/v1/validate",
        headers={"Authorization": token}
    )

    if response.status_code == status.HTTP_200_OK:
        return response.text, None
    else:
        return None, (response.text, response.status_code)