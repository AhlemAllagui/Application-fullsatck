from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'XXXXXXXXXXX'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    "postgresql://postgres:lindybeauty1@localhost:5432/first_app"
)

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150))

    def __init__(self, email, username):
        self.email = email
        self.username = username

# ---- Route pour la page d'accueil ----
@app.route('/')
def home():
    userlist = User.query.all()
    return render_template("home.html", userlist=userlist)


@app.route('/insert', methods=['GET', 'POST'])
def insert(): 
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username') 

        
        check_username = User.query.filter_by(username=username).first()
        check_email = User.query.filter_by(email=email).first()

        if check_username:
            flash('Username already used', category='error') 
        elif check_email:
            flash('Email already used', category='error') 
        elif len(email) < 4:
            flash('Email must be at least 4 characters', category='error')
        elif len(username) < 2:
            flash('Username must be at least 2 characters', category='error')
        else:
            new_user = User(email=email, username=username)
            db.session.add(new_user)
            db.session.commit()
            flash(f'User "{username}" created successfully!', category='success')
            return redirect(url_for("home"))

    return render_template("insert.html") 
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    uto = User.query.get_or_404(id)
    if request.method=='POST':
        email=request.form.get('email')
        username=request.form.get('username')
        
        if uto.email==request.form.get('email'):
            flash('Email already Used ',category='error') 
        elif len(email)<3:
            flash('_> Email > 4 charac',category='error')
        elif len(username)<2:
            flash('_> Username > 4 charac',category='error')
        else:
            uto.email=request.form.get('email')
            uto.username=request.form.get('username')
            db.session.commit()
            flash('User: "'+uto.username+'" Updated',category='success')
        
            return redirect(url_for("home"))
    return render_template("update.html",user=uto) 

@app.route('/delete/<int:id>',methods=['GET','POST'])
def delete_user(id):
        utd = User.query.get_or_404(id)
        username = utd.username
        if utd:
            db.session.delete(utd)
            db.session.commit()
            flash('User: "'+username+'" deleted',category='warning')
            return redirect(url_for("home")) 

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
