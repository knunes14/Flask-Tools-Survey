from flask import Flask, request, render_template, redirect, flash, url_for
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "It's a secret!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def start_survey():
    return render_template('start.html', survey=survey)

@app.route('/answers/<int:question_id>', methods=['POST'])
def handle_answer(question_id):
    answer = request.form.get('answer')
    responses.append(answer)

    if question_id < len(survey.questions):
        return redirect(url_for('question_page', question_id=question_id + 1))
    else:
        return redirect(url_for('thank_you_page'))

@app.route('/thank_you')
def thank_you_page():
    return "Thank You!"

@app.route('/questions/<int:question_id>')
def question_page(question_id):
    if question_id < len(survey.questions):
        question = survey.questions[question_id]
        return render_template('question.html', question=question, question_id=question_id)
    else:
        return redirect(url_for('question_page', question_id=len(survey.questions) - 1))
                        
@app.errorhandler(404)
def page_not_found(error):
    flash("Invalid question number. Redirected to the correct question.")
    return redirect(url_for('question_page', question_id=len(survey.questions) - 1))

if __name__ == '__main__':
    app.run(debug=True)



