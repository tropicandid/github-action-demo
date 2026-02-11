import requests
import sys
import hmac
import hashlib
import datetime as datetime

POST_URL = "https://b12.io/apply/submission"
SIGNING_SECRET = "hello-there-from-b12"

def gh_action_triggered_post_call(github_run_url):
    
    payload = {
        "timestamp": datetime.datetime.now(),
        "name": "Deanna Steers",
        "email": "deanna.steers@gmail.com",
        "resume_link": "https://deannasteers.com/static/docs/DeannaSteers_CV.pdf",
        "repository_link": "https://github.com/tropicandid/github-action-demo",
        "action_run_link": github_run_url
    }

    signature = generate_signature_256(str(payload).encode("utf-8"))

    headers = {
        "Content-Type": "application/json",
        "X-Signature-256": signature,
        "User-Agent":"Mozilla/5.0"  
    }

    try:
        response = requests.post(POST_URL, json=payload, headers=headers)
        response.raise_for_status() 
        print(response.json())
        return response.json()  
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def generate_signature_256(body: bytes) -> str:
    secret = SIGNING_SECRET.encode("utf-8")
    digest = hmac.new(
        key=secret,
        msg=body,
        digestmod=hashlib.sha256
    ).hexdigest()

    return f"sha256={digest}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: Insufficient arguments provided. Please provide a run URL.")
        sys.exit(1)

    run_url = sys.argv[2]
    gh_action_triggered_post_call(run_url)

