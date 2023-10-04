from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SECRET_KEY"] = "app123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)


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

    return render_template("index.html")
    
if __name__=="__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)