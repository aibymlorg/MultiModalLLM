import os
import requests

api_key = "9465237c9264c02fcc35ed78d53f1014e329928901f1c44eb2881e92b029a301"
headers = {"Authorization": f"Bearer {api_key}"}
response = requests.get("https://api.together.xyz/v1/models", headers=headers)
print(response.status_code)  # Should be 200
