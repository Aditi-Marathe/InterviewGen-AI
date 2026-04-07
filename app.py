from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "interviewgenai_secret"  # Needed for session storage

# ---------------- QUESTIONS DATABASE ----------------
questions_db = {
    "data scientist": [
        "What is Machine Learning?",
        "Explain Overfitting",
        "What is supervised learning?",
        "Difference between classification and regression?",
        "What is a confusion matrix?",
        "Explain bias vs variance",
        "What is data preprocessing?",
        "What is Pandas?",
        "Tell me about a data project you worked on",
        "Why do you want to be a Data Scientist?"
    ],
    "web developer": [
        "What is HTML?",
        "Explain CSS",
        "What is JavaScript?",
        "Difference between frontend and backend?",
        "What is responsive design?",
        "Explain DOM",
        "What is Bootstrap?",
        "What is API?",
        "Tell me about your web project",
        "Why do you want to be a Web Developer?"
    ],
    "hr": [
        "Tell me about yourself",
        "What are your strengths?",
        "What are your weaknesses?",
        "Why should we hire you?",
        "Where do you see yourself in 5 years?",
        "Why do you want this job?",
        "Tell me about a challenge you faced",
        "How do you handle pressure?",
        "What motivates you?",
        "Do you have any questions for us?"
    ]
}

# ---------------- KEYWORDS DATABASE ----------------
keywords_db = {
    "What is Machine Learning?": ["data", "model", "learning", "algorithm"],
    "Explain Overfitting": ["training", "test", "overfit", "generalization"],
    "What is HTML?": ["structure", "web", "tags"],
    "Explain CSS": ["style", "design", "layout"],
    "Tell me about yourself": ["student", "skills", "background"],
    "What are your strengths?": ["hardworking", "team", "learning"]
}

# ---------------- CORRECT ANSWERS ----------------
answers_db = {
    "What is Machine Learning?": "Machine Learning is a field of AI where algorithms learn from data to make predictions or decisions.",
    "Explain Overfitting": "Overfitting occurs when a model learns training data too well and performs poorly on unseen data.",
    "What is HTML?": "HTML is a markup language used to structure content on the web.",
    "Explain CSS": "CSS is a style sheet language used to describe the presentation of a document written in HTML.",
    "Tell me about yourself": "A brief introduction about your background, education, skills, and experience.",
    "What are your strengths?": "Strengths are positive personal attributes such as hardworking, teamwork, and problem-solving skills."
}

# ---------------- HOME PAGE ----------------
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['role'] = request.form['role'].lower()
        session['skill'] = request.form['skill']
        # Select 10 questions randomly
        session['questions'] = random.sample(questions_db[session['role']], 10)
        session['current_index'] = 0
        session['results'] = []
        return redirect(url_for('interview'))
    roles = list(questions_db.keys())
    return render_template('index.html', roles=roles)

# ---------------- INTERVIEW PAGE ----------------
@app.route('/interview', methods=['GET', 'POST'])
def interview():
    index = session.get('current_index', 0)
    questions = session.get('questions', [])
    if request.method == 'POST':
        answer = request.form['answer']
        question = questions[index]
        score, feedback, correct_answer = evaluate_answer(question, answer)
        session['results'].append({
            "question": question,
            "user_answer": answer,
            "score": score,
            "feedback": feedback,
            "correct_answer": correct_answer
        })
        session['current_index'] += 1
        if session['current_index'] >= len(questions):
            return redirect(url_for('result'))
        return redirect(url_for('feedback'))
    return render_template('interview.html', question=questions[index])

# ---------------- FEEDBACK PAGE ----------------
@app.route('/feedback')
def feedback():
    index = session.get('current_index', 0)
    result = session['results'][-1]  # Last question
    return render_template('feedback.html', result=result)

# ---------------- FINAL RESULT ----------------
@app.route('/result')
def result():
    results = session.get('results', [])
    total_score = sum([r['score'] for r in results])
    return render_template('result.html', results=results, total_score=total_score)

# ---------------- EVALUATION LOGIC ----------------
def evaluate_answer(question, user_answer):
    keywords = keywords_db.get(question, [])
    score = 0
    for word in keywords:
        if word in user_answer.lower():
            score += 1
    final_score = (score / len(keywords)) * 10 if keywords else 0
    if final_score >= 7:
        feedback = "Excellent Answer 🔥"
    elif final_score >= 4:
        feedback = "Good, but can improve 👍"
    else:
        feedback = "Need improvement ❗"
    correct_answer = answers_db.get(question, "No answer available")
    return round(final_score, 2), feedback, correct_answer

if __name__ == '__main__':
    #app.run(host="0.0.0.0",port=5000, debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
    #app.run(debug=True)