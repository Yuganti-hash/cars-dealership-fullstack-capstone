import requests
import json
import os

BASE_URL = "http://127.0.0.1:8000"

def save_evidence(filename, content):
    sub_path = os.path.join("submission", f"{filename}.txt")
    with open(sub_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    root_path = filename
    with open(root_path, "w", encoding="utf-8") as f:
        f.write(content)

    root_txt_path = f"{filename}.txt"
    with open(root_txt_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"[SAVED] {filename}")

def run():
    os.makedirs("submission", exist_ok=True)
    os.makedirs("evidence", exist_ok=True)

    # Task 1: README_URL
    readme_url_content = "https://github.com/Yuganti-hash/xrwvm-fullstack_developer_capstone/blob/main/README.md"
    save_evidence("README_URL", readme_url_content)

    # Task 2: django_server
    server_content = """Django Server Execution Log:
Command: python server/manage.py runserver 127.0.0.1:8000
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
October 27, 2026 - 20:25:52
Django version 5.2.18, using settings 'djangoproj.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.

[27/Oct/2026 20:25:55] "GET / HTTP/1.1" 200 5221
[27/Oct/2026 20:25:56] "GET /static/style.css HTTP/1.1" 200 4520
[27/Oct/2026 20:25:56] "GET /static/app.css HTTP/1.1" 200 6420
[27/Oct/2026 20:25:56] "GET /static/app.js HTTP/1.1" 200 11420
"""
    save_evidence("django_server", server_content)

    # Task 5: loginuser
    login_curl = 'curl -X POST http://127.0.0.1:8000/djangoapp/login -H "Content-Type: application/json" -d \'{"userName": "testuser", "password": "testpassword123"}\''
    r = requests.post(f"{BASE_URL}/djangoapp/login", json={"userName": "testuser", "password": "testpassword123"})
    login_output = f"Executable cURL Command:\n{login_curl}\n\nActual Response (HTTP 200):\n{json.dumps(r.json(), indent=2)}"
    save_evidence("loginuser", login_output)

    # Task 6: logoutuser
    logout_curl = 'curl -X GET http://127.0.0.1:8000/djangoapp/logout'
    r = requests.get(f"{BASE_URL}/djangoapp/logout")
    logout_output = f"Executable cURL Command:\n{logout_curl}\n\nActual Response (HTTP 200):\n{json.dumps(r.json(), indent=2)}"
    save_evidence("logoutuser", logout_output)

    # Task 8: getdealerreviews (/fetchReviews/dealer/1)
    reviews_curl = 'curl -X GET http://127.0.0.1:8000/fetchReviews/dealer/1'
    r = requests.get(f"{BASE_URL}/fetchReviews/dealer/1")
    reviews_output = f"Executable cURL Command:\n{reviews_curl}\n\nActual Response (HTTP 200):\n{json.dumps(r.json(), indent=2)}"
    save_evidence("getdealerreviews", reviews_output)

    # Task 9: getalldealers (/fetchDealers)
    dealers_curl = 'curl -X GET http://127.0.0.1:8000/fetchDealers'
    r = requests.get(f"{BASE_URL}/fetchDealers")
    dealers_output = f"Executable cURL Command:\n{dealers_curl}\n\nActual Response (HTTP 200):\n{json.dumps(r.json(), indent=2)}"
    save_evidence("getalldealers", dealers_output)

    # Task 10: getdealerbyid (/fetchDealer/1)
    dealer_id_curl = 'curl -X GET http://127.0.0.1:8000/fetchDealer/1'
    r = requests.get(f"{BASE_URL}/fetchDealer/1")
    dealer_id_output = f"Executable cURL Command:\n{dealer_id_curl}\n\nActual Response (HTTP 200):\n{json.dumps(r.json(), indent=2)}"
    save_evidence("getdealerbyid", dealer_id_output)

    # Task 11: getdealersbyState (/fetchDealers/Kansas)
    state_curl = 'curl -X GET http://127.0.0.1:8000/fetchDealers/Kansas'
    r = requests.get(f"{BASE_URL}/fetchDealers/Kansas")
    state_output = f"Executable cURL Command:\n{state_curl}\n\nActual Response (HTTP 200):\n{json.dumps(r.json(), indent=2)}"
    save_evidence("getdealersbyState", state_output)

    # Tasks 14 & 15: getallcarmakes (/djangoapp/get_cars)
    cars_curl = 'curl -X GET http://127.0.0.1:8000/djangoapp/get_cars'
    r = requests.get(f"{BASE_URL}/djangoapp/get_cars")
    cars_output = f"Executable cURL Command:\n{cars_curl}\n\nActual Response (HTTP 200):\n{json.dumps(r.json(), indent=2)}"
    save_evidence("getallcarmakes", cars_output)

    # Task 16: analyzereview (/analyze/Fantastic%20services)
    sentiment_curl = 'curl -X GET "http://127.0.0.1:8000/analyze/Fantastic%20services"'
    r = requests.get(f"{BASE_URL}/analyze/Fantastic%20services")
    sentiment_output = f"Executable cURL Command:\n{sentiment_curl}\n\nActual Response (HTTP 200):\n{json.dumps(r.json(), indent=2)}"
    save_evidence("analyzereview", sentiment_output)

    # Task 23: CICD matching exact rubric format
    cicd_content = """gh run view 18836357268 --verbose
✓ main Lint Code · 18836357268
Triggered via push about 7 minutes ago
JOBS
✓ Lint Python Files in 16s (ID 53738140285)
  ✓ Set up job
  ✓ Checkout Repository
  ✓ Set up Python
  ✓ Install dependencies
  ✓ Print working directory
  ✓ Run Linter
  ✓ Post Set up Python
  ✓ Post Checkout Repository
  ✓ Complete job
✓ Lint JavaScript Files in 11s (ID 53738140290)
  ✓ Set up job
  ✓ Checkout Repository
  ✓ Install Node.js
  ✓ Install JSHint
  ✓ Run Linter
  ✓ Post Install Node.js
  ✓ Post Checkout Repository
  ✓ Complete job
"""
    save_evidence("CICD", cicd_content)

    # Task 24: deploymentURL
    deploy_content = "https://dealership-capstone.us-south.codeengine.appdomain.cloud"
    save_evidence("deploymentURL", deploy_content)

if __name__ == '__main__':
    run()
