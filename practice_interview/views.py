from django.shortcuts import render
import google.generativeai as genai
import os
from django.views import View

from jsonschema import validate
from jsonschema import exceptions

# Define the JSON schema
schema = {
    "type": "object",
    "properties": {
        "job_title": {
            "type": "string",
            "minLength": 1
        },
        "questions": {
            "type": "array",
            "minItems": 5,
            "maxItems": 5,
            "items": {
                "type": "string"
            }
        }
    },
    "required": ["job_title", "questions"]
}

genai.configure(api_key=os.environ["GENAI_API_KEY"])


class InterviewQuestionGenerator:
    def __init__(self, job_title):
        self.job_title = job_title
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_questions(self):
        prompt = f"Generate 5 interview questions for a {self.job_title}."
        response = self.model.generate_content(prompt)
        lines = response.text.split('\n')

        # Keep only lines that start with a number followed by a period (e.g., "1.", "2.", etc.)
        questions = [
            line.strip().replace('*', '') for line in lines
            if (line.strip() and line.strip()[0].isdigit() and line.strip()[1] == '.')
        ]

        return questions


class GenerateInterviewQuestionsView(View):
    def get(self, request):
        return render(request, 'practice.html')

    def post(self, request):
        job_title = request.POST.get('job_title')
        generator = InterviewQuestionGenerator(job_title)
        questions = generator.generate_questions()

        # Validate the response data against the schema
        try:
            validate({'job_title': job_title, 'questions': questions}, schema)
            # Response data is valid, proceed with rendering the template
            return render(request, 'practice.html', {
                'questions': questions,
                'job_title': job_title
            })
        except exceptions.ValidationError as e:
            # Response data is invalid, handle the error
            print(f"Error validating response data: {e}")
            return render(request, 'practice.html', {
                'error': 'Invalid response data',
            })


class EvaluateInterviewAnswersView(View):
    def post(self, request):
        answers = request.POST.getlist('answers')
        feedback = []
        job_title = request.POST.get('job_title')
        generator = InterviewQuestionGenerator(job_title)

        # Retrieve questions that were stored in the hidden input fields
        questions = []
        for i in range(1, 6):
            question = request.POST.get(f'question_{i}')
            if question:
                questions.append(question)

        if len(questions) != len(answers):
            return render(request, 'practice.html', {
                'error': 'Mismatch between questions and answers',
            })

        # Now, evaluate the answers based on the retrieved questions
        for i, answer in enumerate(answers):
            question = questions[i]
            print(f"Question: {question}")
            print(f"Answer: {answer}")
            print(f"Index: {i+1}")

            # Uncomment to evaluate the answer using the model
            prompt = (
                f"Evaluate the following answer to the question '{question}':\n\n"
                f"Answer: {answer}"
            )
            # Simulate a response from the AI
            response = generator.model.generate_content(prompt)
            feedback.append(response.text.strip().replace('*', ''))

        return render(request, 'practice.html', {
            'answers': answers,
            'feedback': feedback,
            'job_title': job_title,
            'questions': questions,  # Include the questions for context
        })
