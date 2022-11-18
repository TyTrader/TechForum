from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import generate_password_hash, check_password_hash
from database import User, Question

app = Flask(__name__)
app.secret_key = "fortune5000gonedown"

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        userName = request.form["u_name"]
        userEmail = request.form["u_email"]
        userPassword = request.form["u_pass"]
        encryptedUserPassword = generate_password_hash(userPassword)
        User.create(name=userName, email=userEmail, password=encryptedUserPassword)
        flash("User created successfully")
    return render_template("signup.html")


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        userEmail = request.form["u_email"]
        userPassword = request.form["u_pass"]
        try:
            user = User.get(User.email == userEmail)
            encryptedPassword = user.password
            if check_password_hash(encryptedPassword, userPassword):
                flash("Login is Successful")
                session["loggedIn"] = True
                session["userName"] = user.name

                return redirect(url_for("home"))
        except:
            flash("Wrong Email/Password")

    return render_template("login.html")


@app.route("/home")
def home():
    if not session["loggedIn"]:
        return redirect(url_for("login"))
    return render_template("home.html")


@app.route("/addQuestions", methods=['GET', 'POST'])
def addQuestion():
    if not session["loggedIn"]:
        return redirect(url_for("login"))
    if request.method == "POST":
        questionName = request.form["name"]
        questionAnswer = request.form["answer"]
        Question.create(question=questionName, answer=questionAnswer)

        flash("Question created successfully")

    return render_template("addQuestion.html")


@app.route("/questions")
def question():
    if not session["loggedIn"]:
        return redirect(url_for("login"))
    questions = Question.select()
    return render_template("questions.html", questions=questions)


@app.route("/delete/<int:id>")
def delete(id):
    if not session["loggedIn"]:
        return redirect(url_for("login"))
    Question.delete().where(Question.id == id).execute()
    flash("Question deleted successfully")
    return redirect(url_for("questions"))


@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    if not session["loggedIn"]:
        return redirect(url_for("login"))

    question = Question.get(Question.id == id)
    if request.method == 'POST':
        updatedQuestion = request.form['name']
        updatedAnswer = request.form['answer']
        question.name = updatedQuestion
        question.answer = updatedAnswer
        question.save()
        flash('Question answered successfully')
        return redirect(url_for("questions"))
    return render_template("answerQuestion.html", question=question)


if __name__ == '__main__':
    app.run(debug=True)
