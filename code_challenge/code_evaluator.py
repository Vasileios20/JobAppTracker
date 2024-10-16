import requests
import time
import os

RAPID_API_KEY = os.environ.get("RAPID_API_KEY")


class CodeEvaluator:
    def __init__(self):
        self.api_url = "https://judge0-ce.p.rapidapi.com/submissions"
        self.headers = {
            'X-RapidAPI-Key': RAPID_API_KEY,
            'X-RapidAPI-Host': 'judge0-ce.p.rapidapi.com',
        }
        if not RAPID_API_KEY:
            raise ValueError("RAPID_API_KEY environment variable not set!")

    def evaluate(self, source_code, language_id, stdin=''):
        # Prepare the request payload
        payload = {
            'source_code': source_code,
            'language_id': language_id,
            'stdin': stdin,  # Send any input required for the program
        }

        # Make the initial request to submit the code
        try:
            response = requests.post(
                self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()  # Raises an error for bad responses
        except requests.exceptions.RequestException as e:
            return {"error": f"Error in submission request: {e}"}

        submission = response.json()

        # Wait for the result to be processed
        result_url = f"{self.api_url}/{submission['token']}"
        result = None
        while True:
            try:
                result_response = requests.get(
                    result_url, headers=self.headers)
                result_response.raise_for_status()
            except requests.exceptions.RequestException as e:
                return {"error": f"Error in result retrieval: {e}"}

            result = result_response.json()

            # If the status ID is 3 or higher, we have the result
            if result['status']['id'] > 2:
                break

            time.sleep(2)  # Wait before checking again

        # Format the result into a user-friendly structure
        formatted_result = {
            # Safely handle None
            'stdout': (result.get('stdout') or '').strip(),
            # Safely handle None
            'stderr': (result.get('stderr') or '').strip(),
            'status': result['status']['description'],
            'time': result['time'],
            'memory': result['memory'],
        }

        return formatted_result
