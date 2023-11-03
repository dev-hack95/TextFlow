import os
import requests
from fastapi import status

def login(request):
    auth = request.authorization
    if not auth:
        return None, ("Missing Credentials", status.HTTP_401_UNAUTHORIZED)
    
    basicAuth = (auth.username, auth.password)

    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/v1/login",
        auth=basicAuth
    )

    if response.status_code == status.HTTP_200_OK:
        return  response.text, None
    else:
        return None, (response.text, f"Authentication failed with code {response.status_code}", status.HTTP_503_SERVICE_UNAVAILABLE)