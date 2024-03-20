
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import os
from werkzeug.utils import secure_filename

# папка для сохранения загруженных файлов


app = Flask(__name__)
app.secret_key = 'SecterKeyforhack'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

UPLOAD_FOLDER = 'static/img/'
# расширения файлов, которые разрешено загружать
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'DNG', 'raw', 'mp4'}


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
manager = LoginManager(app)

app.app_context().push()


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(32), nullable = False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(32),nullable=False)
    last_name = db.Column(db.String(32), nullable=False, default=False)
    admin = db.Column(db.Boolean(), nullable=False, default=False)
    avatar = db.Column(db.String(400), default="")
    albums = db.relationship("Albums", backref="users")
    content = db.relationship("Content", backref="users")

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(400))
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    album = db.Column(db.Integer, db.ForeignKey("albums.id"))
    location = db.Column(db.String(50))
    date = db.Column(db.Date)
    device = db.Column(db.String(50))


class Albums(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    authors = db.Column(db.Integer, db.ForeignKey("users.id"))
    description = db.Column(db.Integer)
    tegs = db.Column(db.String(50), default="")
    date = db.Column(db.Date, default="")
    data_add_alb = db.Column(db.Date, default="")
    album = db.relationship("Content", backref="albums")

db.create_all()

@manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

@app.route("/")
@app.route("/general")
def general():
    posts = Content.query.all()
    return render_template('general.html',posts=posts)

@app.route("/profile")
def profile():
    posts = Content.query.filter_by(author_id=current_user.id)
    return render_template('profile.html', posts=posts)

@app.route("/out_akk")
def logout():
    logout_user()
    return redirect('general')

@app.route("/reg", methods=['GET','POST'])
def reg():
    if current_user.is_authenticated:
        return redirect(url_for('general'))
    else:
        fname = ''
        lname = ''
        login = ''
        password = ''
        password2 = ''
        if request.method =='POST':
            fname = request.form.get('fname')
            lname = request.form.get('lname')
            login = request.form.get('login')
            password = request.form.get('password')
            print(password)
            password2 = request.form.get('confirm_password')
            try:
                user = Users.query.filter_by(login=login).first()
                print(user.login)
                flash('Этот логин уже зарегистрирован')
                login = ''
            except:
                if password == password2:
                    password = generate_password_hash(password)
                    user = Users(login=login, password=password, first_name=fname, last_name=lname, admin=0, avatar='mjkk')
                    db.session.add(user)
                    db.session.commit()
                    login_user(user)
                    return redirect(url_for('general'))
                else:
                    flash('пароли не совпадают')
                    password = ''
                    password2 = ''
    return render_template('registration.html')

@app.route("/log", methods=['GET','POST'])
def log():
    # if current_user.is_authenticated:
    #     return redirect(url_for('general'))
    # else:
        login = ''
        password = ''
        if request.method == 'POST':
            login = request.form.get('login')
            password = request.form.get('password')
            if login and password:
                try:

                    user = Users.query.filter_by(login=login).first()
                    if check_password_hash(user.password, password):
                        login_user(user)

                        return redirect(url_for('general'))
                    else:

                        flash('Неверный пароль')
                        password = ''
                except:
                    flash('Пользователь не найден')
                    login = ''
                    password = ''
            else:
                flash('Введите логин и пароль')
        return render_template('auth.html',login=login)

@app.route("/af",  methods=['GET','POST'])
def add_file():


    if request.method == 'POST':
        # filename = request.form.get('add_f')
        file = request.files['add_f']
        filename = secure_filename(file.filename)
        pathfile = 'static/img/'+filename
        print(pathfile)
        content = Content(url=pathfile, author_id = current_user.id, album=1, location="", date=datetime.date.today(), device="efe")
        db.session.add(content)
        db.session.commit()
        print(file)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('profile'))

    return render_template("add_file.html")

@app.route("/red01")
def red01():
    return render_template('redact.html')

@app.route("/create_albums")
def create_albums():
    posts = Content.query.all()
    return render_template('create_albums.html', posts=posts)

if __name__ == "__main__":
    app.run(debug=True)
