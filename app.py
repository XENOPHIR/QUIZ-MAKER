from flask import Flask, render_template, request, redirect, url_for, session
from config import Config
from models import db, Question, QuizSession, UserAnswer
from questions_parser import parse_questions_from_txt
from sqlalchemy.orm import joinedload
import random

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    with app.app_context():
        db.create_all()

    quiz_id = session.get('quiz_id')
    if quiz_id:
        cleanup_quiz_session(quiz_id)
        session.pop('quiz_id', None)

    if request.method == 'POST':
        file = request.files['file']
        if not file:
            return "No file uploaded", 400

        try:
            questions_data = parse_questions_from_txt(file)
        except Exception as e:
            return f"❌ Error while parsing: {e}", 500

        print(f"\n✅ Parsed {len(questions_data)} questions.\n")

        with open("parsed_output.txt", "w", encoding="utf-8") as out:
            for i, q in enumerate(questions_data, start=1):
                print(f"{i}. {q['text']}")
                print(f"   A. {q['option_a']}")
                print(f"   B. {q['option_b']}")
                print(f"   C. {q['option_c']}")
                print(f"   D. {q['option_d']}")
                print(f"   ✔ Correct: {q['correct']}\n")

                out.write(f"{i}. {q['text']}\n")
                out.write(f"A. {q['option_a']}\n")
                out.write(f"B. {q['option_b']}\n")
                out.write(f"C. {q['option_c']}\n")
                out.write(f"D. {q['option_d']}\n")
                out.write(f"ANSWER: {q['correct']}\n\n")

        # Заносим в базу данных
        for q in questions_data:
            question = Question(
                text=q['text'],
                option_a=q['option_a'],
                option_b=q['option_b'],
                option_c=q['option_c'],
                option_d=q['option_d'],
                correct=q['correct']
            )
            db.session.add(question)
        db.session.commit()

        return redirect(url_for('quiz'))

    return render_template('index.html')

@app.route('/quiz')
def quiz():
    questions = Question.query.order_by(db.func.rand()).all()
    session['question_ids'] = [q.id for q in questions]
    return render_template('quiz.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    question_ids = session.get('question_ids', [])
    score = 0
    total = len(question_ids)

    quiz_session = QuizSession(score=0, total=total)
    db.session.add(quiz_session)
    db.session.flush() 

    for qid in question_ids:
        question = Question.query.get(qid)
        selected = request.form.get(str(qid))
        is_correct = (selected == question.correct)
        if is_correct:
            score += 1

        answer = UserAnswer(
            quiz_id=quiz_session.id,
            question_id=qid,
            selected=selected,
            is_correct=is_correct
        )
        db.session.add(answer)

    quiz_session.score = score
    db.session.commit()
    return redirect(url_for('result', quiz_id=quiz_session.id))

def cleanup_quiz_session(quiz_id):
    quiz = QuizSession.query.options(joinedload(QuizSession.answers)).get(quiz_id)
    if not quiz:
        return

    question_ids = [answer.question_id for answer in quiz.answers]

    for answer in quiz.answers:
        db.session.delete(answer)

    db.session.delete(quiz)

    for qid in set(question_ids):
        question = Question.query.get(qid)
        if question:
            db.session.delete(question)

    db.session.commit()

@app.route('/result/<int:quiz_id>')
def result(quiz_id):
    quiz = QuizSession.query.get_or_404(quiz_id)
    answers = UserAnswer.query.filter_by(quiz_id=quiz.id).all()

    rendered = render_template('result.html', quiz=quiz, answers=answers)

    cleanup_quiz_session(quiz_id)
    session.clear()

    return rendered

@app.route('/cancel', methods=['POST'])
def cancel_quiz():
    question_ids = session.get('question_ids', [])

    for qid in question_ids:
        q = Question.query.get(qid)
        if q:
            db.session.delete(q)

    db.session.commit()
    session.pop('question_ids', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
