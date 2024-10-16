
# Git Hired 🚀

## Because your job hunt shouldn't feel like searching for a needle in a digital haystack!

Welcome to Git Hired, your new best friend in the job application jungle. Born in the crucible of the Elevate Hackathon, Git Hired is here to turn your job search from a chaotic mess into a well-oiled machine. (We can't guarantee you'll get hired, but at least you'll know where you applied!)

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [The Dream Team](#the-dream-team)
- [License](#license)

# User Stories

1. **As a job seeker**, I want to enter my job title so that I can generate relevant interview questions tailored to my role.

2. **As a job seeker**, I want to view a list of generated interview questions after submitting my job title.

3. **As a job seeker**, I want to provide my answers to the generated questions and submit them for evaluation.

4. **As a user**, I want to see AI-generated feedback on my answers.

5. **As a user**, I want to revisit previously generated questions and answers.

6. **As an administrator**, I want to manage user submissions and feedback.

7. **As a new user**, I want an intuitive interface that guides me through the process.

8. **As a user**, I want to receive success messages after successfully generating questions or submitting answers.


## Features

- **Application Tracking**: Keep tabs on your job applications like a pro stalker (but legal and for your own stuff).
- **Dashboard View**: Get a bird's eye view of your job hunt. It's like Google Maps, but for your career!
- **Search and Filter**: Find that one application faster than you can say "I'm perfect for this job!"
- **Status Updates**: From "Applied" to "Hired" (or "They ghosted me"), track it all.
- **Notes and Comments**: For when you need to remember that the interviewer had a cat named "Mr. Whiskers" (it might be important, you never know).
- **Analytics**: Impress your friends with fancy graphs about your job search. Who said unemployment can't be fun?

## Installation

1. Clone the repo:
   ```
   git clone https://github.com/your-username/git-hired.git
   ```
2. Navigate to the project directory:
   ```
   cd git-hired
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up the database:
   ```
   python manage.py migrate
   ```
5. Start the server:
   ```
   python manage.py runserver
   ```

## Usage

1. Create an account (we promise we won't sell your data to job recruiters... or will we? 👀)
2. Log in and start adding your job applications
3. Use the dashboard to track your progress
4. Update application statuses as you go
5. Celebrate when you finally Git Hired! 🎉

## API Documentation

For those who like to peek under the hood, check out our [API documentation](link-to-your-api-docs).

## Contributing

We welcome contributions! Please check out our [Contributing Guide](link-to-contributing-guide) for details on how to get started. Don't worry, we don't bite (unless you write bugs, then we might nibble a little).

## The Dream Team

Meet the caffeinated coders behind Git Hired:

### Vasi "The Visionary" 👁️
- Frontend Maestro
- Turns caffeine into pixel-perfect UIs
- [GitHub](https://github.com/vasi) | [LinkedIn](https://linkedin.com/in/vasi)

### Erin "The Energizer" ⚡
- Full Stack Dynamo
- Codes faster than the speed of light (almost)
- [GitHub](https://github.com/erin) | [LinkedIn](https://linkedin.com/in/erin)

### David "The Debugger" 🐛
- Backend Sorcerer
- Can smell a bug from a mile away
- [GitHub](https://github.com/david) | [LinkedIn](https://linkedin.com/in/david)

### Ciaran "The Connector" 🔗
- API Alchemist
- Connects dots and databases with equal ease
- [GitHub](https://github.com/ciaran) | [LinkedIn](https://linkedin.com/in/ciaran)

### Marlon "The Mastermind" 🧠
- Architecture Aficionado
- Builds systems that even Skynet would envy
- [GitHub](https://github.com/marlon) | [LinkedIn](https://linkedin.com/in/marlon)

### Kim "The Kode Whisperer" 🤫
- UX/UI Enchanter
- Makes our app look prettier than your Instagram feed
- [GitHub](https://github.com/kim) | [LinkedIn](https://linkedin.com/in/kim)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details. (It's MIT because we're too busy job hunting to write our own license.)

---

Remember, in the world of job hunting, it's not about the destination, it's about the journey. And with Git Hired, at least that journey will be well-documented! Happy job hunting! 🎉

## Entity-Relationship Diagram (ERD) Design

### Wireframes

* We used [Balsamiq](https://balsamiq.com/wireframes) to design the wireframes for us website.

#### Desktop:
<details>

![Desktop Home page]()

![Desktop About page]()

![Desktop Job Application page]()

![Desktop Practice Interview page]()

</details>

## Performance

The Git Hired website was assessed with Google Lighthouse via Google Chrome Developer Tools. Performance scores were evaluated for both desktop and mobile devices.

### Desktop Performance
- The average score for the pages was 90/100 and the majority of the pages getting an excellent performance of over 90/100

| **Tested** | **Performance Score** | **View Result** | **Pass** |
--- | --- | --- | :---:
|index| 95 / 100 | <details><summary>Screenshot of result</summary>![Result]()</details> | :white_check_mark:
|about| 85 / 100 | <details><summary>Screenshot of result</summary>![Result]()</details> | :white_check_mark:
|Job Application| 99 / 100 | <details><summary>Screenshot of result</summary>![Result]()</details> | :white_check_mark:
|Practice| 74 / 100 | <details><summary>Screenshot of result</summary>![Result]()</details> | :white_check_mark:


### Mobile Performance
- The average score for the pages was 80/100 and the majority of the pages getting an good performance of 70/100

| **Tested** | **Performance Score** | **View Result** | **Pass** |
--- | --- | --- | :---:
|index| 95 / 100 | <details><summary>Screenshot of result</summary>![Result]()</details> | :white_check_mark:
|about| 85 / 100 | <details><summary>Screenshot of result</summary>![Result]()</details> | :white_check_mark:
|Job Application| 99 / 100 | <details><summary>Screenshot of result</summary>![Result]()</details> | :white_check_mark:
|Practice| 74 / 100 | <details><summary>Screenshot of result</summary>![Result]()</details> | :white_check_mark:

[Return to Table of Contents](#table-of-contents)

## Code Validation

### HTML Validation
ll pages were validated, and the code was pasted in. A filter was applied to remove issues related to the Django templating system. 

| **Tested** | **Result** | **View Result** | **Pass** |
--- | --- | --- | :---:
|base| No errors | <details><summary>Screenshot of result</summary>![Result]()</details>| :white_check_mark:
|index| No errors | <details><summary>Screenshot of result</summary>![Result]()</details>| :white_check_mark:
|about| No errors | <details><summary>Screenshot of result</summary>![Result]()</details>| :white_check_mark:
|Job Application| No errors | <details><summary>Screenshot of result</summary>![Result]()</details>| :white_check_mark:
|Practice| No errors | <details><summary>Screenshot of result</summary>![Result]()</details>| :white_check_mark:


### CSS Validation

| **Tested** | **Result** | **View Result** | **Pass** |
--- | --- | --- | :---:
|styles.css | No errors |<details><summary>Screenshot of result</summary>![Result]()</details>| :white_check_mark:

## Acknowledgements

[Ciaran Griffin](https://github.com/ciarangriffin93)<br>
[David Cotter](https://github.com/trxdave)<br>
[Erin Doyle](https://github.com/erinvdoyle)<br>
[Kim Halon](https://github.com/kimatron)<br>
[Vasilis](https://github.com/Vasileios20)