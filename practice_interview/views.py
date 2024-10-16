from django.shortcuts import render
import google.generativeai as genai
import os
from django.views import View
from jsonschema import validate, exceptions

API_KEY = os.getenv("GENAI_API_KEY")

# Configure the Google Generative AI API key
genai.configure(api_key=API_KEY)


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


class InterviewQuestionGenerator:
    def __init__(self, job_title):
        self.job_title = job_title
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_questions(self):
        prompt = f"Generate 5 interview questions for a {self.job_title}."
        response = self.model.generate_content(prompt)
        lines = response.text.split('\n')

        # Filter and format the questions
        questions = [
            line.strip().replace('*', '') for line in lines
            if (
                line.strip() and
                line.strip()[0].isdigit() and
                line.strip()[1] == '.'
            )
        ]

        return questions


class GenerateInterviewQuestionsView(View):
    def get(self, request):
        return render(request, 'practice.html')

    def post(self, request):
        job_title = request.POST.get('job_title')
        generator = InterviewQuestionGenerator(job_title)
        questions = generator.generate_questions()

        try:

            # Validate the generated questions against the schema
            validate({'job_title': job_title, 'questions': questions}, schema)

            return render(request, 'practice.html', {
                'questions': questions,
                'job_title': job_title
            })
        except (exceptions.ValidationError, Exception) as e:
            print(f"Error: {e}")
            return render(request, 'practice.html', {
                'error': 'Failed to generate valid questions.',
            })


class EvaluateInterviewAnswersView(View):
    def post(self, request):
        answers = request.POST.getlist('answers')
        job_title = request.POST.get('job_title')
        generator = InterviewQuestionGenerator(job_title)

        # Retrieve questions from the form
        questions = [request.POST.get(f'question_{i}') for i in range(
            1, 6) if request.POST.get(f'question_{i}')]

        if len(questions) != len(answers):
            return render(request, 'practice.html', {
                'error': 'Mismatch between questions and answers.',
            })

        evaluation_data = []
        for i, answer in enumerate(answers):
            question = questions[i]
            prompt = (
                f"Evaluate the following answer to the question '{question}':"
                f"\n\n"
                f"Answer: {answer}"
            )

            # Generate feedback using the model
            try:
                response = generator.model.generate_content(prompt)
                feedback = response.text.strip().replace('*', '')
                evaluation_data.append((question, answer, feedback))
            except Exception as e:
                evaluation_data.append(
                    (question, answer, f"Error generating feedback: {e}"))

        return render(request, 'practice.html', {
            'evaluation_data': evaluation_data,
            'job_title': job_title,
        })
