from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = "app123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "chinmays117@gmail.com"
app.config["MAIL_PASSWORD"] = os.getenv("PASSWORD")

db = SQLAlchemy(app)

mail = Mail(app)

class Form(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(88))
    surname = db.Column(db.String(88))
    email = db.Column(db.String(88))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(88))

@app.route("/", methods=["GET","POST"])
def index():
    if request.method=="POST":
        # the method looks for the 'name' attribute of the tags in <div>
        
        first_name = request.form["first-name"]
        last_name = request.form["last-name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = datetime.strptime(date,"%Y-%m-%d")
        occupation = request.form["occupation"]

        form = Form(name=first_name,surname=last_name,email=email,date=date_obj,occupation=occupation)
        db.session.add(form)
        db.session.commit()
        message_body = f"Thank you for your submission, {first_name}! Here are the details we received:\n"\
        f"your name: {first_name},\n last name: {last_name} \n date:{date}\n We will get in touch soon!"
        message=Message(subject="New Form Submission",sender=app.config["MAIL_USERNAME"],
                recipients=[email],body=message_body)
        mail.send(message)
        flash(f"{first_name}, your form was sent successfully!","success")

    return render_template("index.html")
    
if __name__=="__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)