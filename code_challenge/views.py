from django.shortcuts import render
from .leetcode_fetcher import LeetCodeChallengeFetcher
from .code_evaluator import CodeEvaluator


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

        # Check if the output matches the expected output
        passed = evaluation_result['stdout'] == expected_output
        context = {
            'passed': passed,
            'source_code': source_code,
            'language': language,
            'expected_output': expected_output,
            'evaluation_result': evaluation_result,
        }

        # return JsonResponse({
        #     'passed': passed,
        #     'result': evaluation_result,
        # })

    return render(request, 'code_submission.html', context)
