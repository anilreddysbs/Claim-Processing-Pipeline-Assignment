import requests
import time
import os

URL = "http://127.0.0.1:8000/api/process"
FILE_PATH = "final.pdf"

def test_api():
    print("Waiting for server to start...")
    time.sleep(5) # Give uvicorn some time to start

    if not os.path.exists(FILE_PATH):
        print(f"Error: {FILE_PATH} not found.")
        return

    print(f"Sending request to {URL}...")
    try:
        start_time = time.time()
        with open(FILE_PATH, 'rb') as f:
            files = {'file': (FILE_PATH, f, 'application/pdf')}
            data = {'claim_id': 'TEST-CLAIM-001'}
            response = requests.post(URL, files=files, data=data)
        end_time = time.time()
        
        print(f"Time Taken: {end_time - start_time:.2f} seconds")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Response JSON:")
            print(response.json())
        else:
            print("Error Response:")
            print(response.text)
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_api()
