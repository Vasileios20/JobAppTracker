from django.shortcuts import render
from .leetcode_fetcher import LeetCodeChallengeFetcher
from .code_evaluator import CodeEvaluator
import google.generativeai as genai
import os

API_KEY = os.getenv("GENAI_API_KEY")
genai.configure(api_key=API_KEY)


def code_challenge_view(request):
    difficulty = request.GET.get('difficulty', 'easy')  # Default to easy
    fetcher = LeetCodeChallengeFetcher()
    challenges = fetcher.get_challenges(difficulty=difficulty)
    return render(
        request,
        'challenge_list.html',
        {'challenges': challenges, 'difficulty': difficulty}
    )


def challenge_detail_view(request, slug):
    fetcher = LeetCodeChallengeFetcher()
    challenge = fetcher.get_challenge_details(slug)

    if not challenge:
        return render(request, '404.html', status=404)

    return render(request, 'challenge_detail.html', {'challenge': challenge})


def submit_solution(request):
    if request.method == 'POST':
        source_code = request.POST.get('source_code')
        language = request.POST.get('language')  # e.g., 'python'
        expected_output = request.POST.get('expected_output')
        challenge = request.POST.get('challenge')
        example_test_case = request.POST.get('example_test_case')

        # Map language to the corresponding Judge0 ID (e.g., Python -> 71)
        language_map = {
            'python': 71,
            'javascript': 63,
            'cpp': 54,
            # Add more languages as needed
        }
        language_id = language_map.get(language)

        evaluator = CodeEvaluator()
        evaluation_result = evaluator.evaluate(
            source_code, language_id, expected_output)

        actual_output = evaluation_result.get('stdout', '')
        expected_output = expected_output.strip()

        # Check if the output matches the expected output
        passed = actual_output == expected_output

        # Generate AI feedback based on the evaluation result
        feedback_prompt = (
            f"Here is the challenge prompt:\n{challenge}\n\n"
            f"Here is the code:\n{source_code}\n\n"
            f"Language: {language}\n\n"
            f"If there is Example test case:{example_test_case}\n"
            f"If there is The actual output is:\n{actual_output}\n\n"
            f"Please compare the challenge prompt to source code and give feedback."
        )

        try:
            feedback_response = genai.GenerativeModel(
                "gemini-1.5-flash").generate_content(feedback_prompt)
            feedback = feedback_response.text.strip().replace('*', '')
        except Exception as e:
            feedback = f"Error generating feedback: {e}"

        context = {
            'passed': passed,
            'source_code': source_code,
            'language': language,
            'expected_output': expected_output,
            'actual_output': actual_output,
            'evaluation_result': evaluation_result,
            'ai_feedback': feedback,  # Add AI feedback here
        }
        return render(request, 'code_submission.html', context)
    return render(request, 'code_submission.html', context)
