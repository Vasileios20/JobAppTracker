import requests
import json


class LeetCodeChallengeFetcher:
    def __init__(self):
        self.problem_base_url = "https://leetcode.com/problems/"
        self.graphql_url = "https://leetcode.com/graphql/"

    def get_challenges(self, difficulty=None):
        """
        Fetch all challenges. Difficulty can be 'easy', 'medium', or 'hard'.
        """
        base_url = "https://leetcode.com/api/problems/all/"
        response = requests.get(base_url)
        if response.status_code == 200:
            problems = response.json().get('stat_status_pairs', [])
            # Optionally filter by difficulty
            if difficulty:
                difficulty_level = self.get_difficulty_level(difficulty)
                problems = [p for p in problems if p['difficulty']
                            ['level'] == difficulty_level]
            return self._format_problems(problems)
        return []

    def _format_problems(self, problems):
        """
        Format problems to include title, slug, difficulty, and URLs.
        """
        formatted_problems = []
        for problem in problems:
            formatted_problems.append({
                'title': problem['stat']['question__title'],
                'slug': problem['stat']['question__title_slug'],
                'difficulty': self.get_difficulty_name(problem['difficulty']['level']),
                'paid_only': problem['paid_only'],
                'url': f"{self.problem_base_url}{problem['stat']['question__title_slug']}/"
            })
        return formatted_problems

    def get_challenge_details(self, slug):
        """
        Fetch detailed information for a specific challenge by its slug.
        This includes the description, sample inputs/outputs, etc.
        """
        query = """
        query getQuestionDetail($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                title
                content
                difficulty
                likes
                dislikes
                similarQuestions
                exampleTestcases
            }
        }
        """
        variables = {"titleSlug": slug}
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(self.graphql_url, json={
                                 "query": query, "variables": variables}, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data.get('data', {}).get('question', {})
        else:
            return {}

    def get_difficulty_level(self, difficulty):
        """
        Convert difficulty name to LeetCode difficulty level (1, 2, 3).
        """
        difficulty_mapping = {'easy': 1, 'medium': 2, 'hard': 3}
        return difficulty_mapping.get(difficulty.lower())

    def get_difficulty_name(self, level):
        """
        Convert numeric difficulty level to readable difficulty name.
        """
        difficulty_mapping = {1: 'Easy', 2: 'Medium', 3: 'Hard'}
        return difficulty_mapping.get(level, 'Unknown')
