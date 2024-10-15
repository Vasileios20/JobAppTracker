import requests
import time
import os

RAPID_API_KEY = os.environ.get("RAPID_API_KEY")


class CodeEvaluator:
    def __init__(self):
        self.api_url = "https://judge0-ce.p.rapidapi.com/submissions"
        self.headers = {
            'X-RapidAPI-Key': RAPID_API_KEY,  # Replace with your Judge0 API key
            'X-RapidAPI-Host': 'judge0-ce.p.rapidapi.com',
        }

    def evaluate(self, source_code, language_id, expected_output):
        # Prepare the request payload
        payload = {
            'source_code': source_code,
            # LeetCode is typically Python (ID: 71)
            'language_id': language_id,
            'stdin': '',  # Add any input if required
            'expected_output': expected_output,
        }

        # Make the initial request to submit the code
        response = requests.post(
            self.api_url, headers=self.headers, json=payload)
        submission = response.json()

        # Wait for the result to be processed
        result_url = f"{self.api_url}/{submission['token']}"
        result = None
        while True:
            result_response = requests.get(result_url, headers=self.headers)
            result = result_response.json()
            if result['status']['id'] > 2:  # Status code 3 means "Completed"
                break
            time.sleep(2)  # Wait a bit before rechecking

        # Return the evaluation result
        return result
