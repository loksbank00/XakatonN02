
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import os
from werkzeug.utils import secure_filename
from transliterate import translit

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


class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(400))
    ext = db.Column(db.String(5))
    author_id = db.Column(db.ForeignKey("users.id"))
    autor_login = db.Column(db.String(50))
    album = db.Column(db.ForeignKey("albums.id"))
    location = db.Column(db.String(50))
    date = db.Column(db.Date)
    device = db.Column(db.String(50))
    tegs = db.Column(db.String(150), default="")


class Albums(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), default="")
    authors = db.Column( db.ForeignKey("users.id"))
    description = db.Column(db.String(500))
    tegs = db.Column(db.String(150), default="")
    date = db.Column(db.Date, default="")
    data_add_alb = db.Column(db.Date, default="")
    access = db.Column(db.Integer, default="0")
    content = db.Column(db.String(100), default="")


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
    alb = Albums.query.filter_by(authors=current_user.id)
    posts = Content.query.filter_by(author_id=current_user.id)
    return render_template('profile.html', posts=posts, alb=alb)

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

    ras='jkl'
    if request.method == 'POST':
        # filename = request.form.get('add_f')
        file = request.files['add_f']
        if file.filename[1] in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя':
            filename = translit(file.filename[:-4],'ru')+file.filename[-4:]
        else:
            filename = secure_filename(file.filename)
        print(filename)
        ras1, ras = os.path.splitext(filename)
        print(ras)
        pathfile = UPLOAD_FOLDER+filename
        print(pathfile)
        autor_login = Users.query.filter_by(id=current_user.id).first()
        tegs = request.form.get('tegs_a')
        content = Content(tegs=tegs, autor_login=autor_login.login , url=pathfile, ext=ras, author_id = current_user.id, album=0, location="", date=datetime.date.today(), device="efe")
        db.session.add(content)
        db.session.commit()
        print(file)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('profile'))

    return render_template("add_file.html")

@app.route("/red01")
def red01():
    return render_template('redact.html')

@app.route("/create_albums",   methods=['GET','POST'])
def create_albums():
    posts = Content.query.filter_by(author_id=current_user.id)
    if request.method == 'POST':
        print("sdfgkj")

        authors = request.form.get('authors')
        photos = request.form.get('photo_list').split(' ')
        for i in range(len(photos)):
            if photos[i] =='':
                photos.remove(photos[i])
            else:
                photos[i]=int(photos[i])
        print(photos)
        name = request.form.get('name')
        print(type(name))
        tegs = request.form.get('tegs')
        description = request.form.get('description')
        access = int(request.form.get('access'))
        print(type(access))
        print(current_user)
        contentinalbum =1
        albm = Albums(name=name, tegs=tegs, authors=current_user.id, description=description, date=datetime.date.today(), data_add_alb=datetime.date.today(),  access=access, content=str(photos))
        print("asdasdasd")
        db.session.add(albm)
        print("al")
        db.session.commit()


    return render_template('create_albums.html', posts=posts)


if __name__ == "__main__":
    app.run(debug=True)
