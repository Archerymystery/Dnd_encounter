from flask import Flask, render_template,request,redirect,url_for,flash
from werkzeug.security import check_password_hash, generate_password_hash
from config import Config
from models import db, Player,PlayerImg,User
from extensions import db, login_manager
from flask_login import login_user, logout_user, login_required, current_user
from forms import LoginForm, RegistrationForm
import random

from admin import admin
import os
import time
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
admin.init_app(app)
login_manager.init_app(app)
with app.app_context():
    db.create_all()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
@app.route("/")
@login_required
def index():
    user = current_user

    players = Player.query.filter_by(user_id=user.id).order_by(Player.init.desc()).all()
    counter=user.counter
    selected = request.args.get('selected')
    if len(players)==0:
        return render_template("index.html",selected=None,counter=None,players=[])

    if selected is None:
        selectedPlayer = players[counter]
    else:
        selectedPlayer = Player.query.get(int(selected))
    print(players)
    return render_template("index.html",selected=selectedPlayer,counter=players[counter],players=players)
@app.route("/add", methods=["POST","GET"])
def add_player():
    user= current_user
    if request.method=="GET":
        return render_template("add.html")
    if request.method=="POST":
        name = request.form.get("name", "").strip()
        if name:
            speed = int(request.form.get("speed", "1"))
            ac = int(request.form.get("ac", "1"))
            hp_max = int(request.form.get("hp", "1"))
            initative = int(request.form.get("initative", "1"))
            level = int(request.form.get("level", "1"))
            player = Player(name=name,speed=speed,hp_max=hp_max,hp=hp_max,init=initative,ac=ac,lv=level,user_id=user.id)
            file= request.files.get("img")
            k=False
            # for file in files:
            print(file)
            if file and allowed_file(file.filename):
                filename=f"{round(time.time()*1000)}{os.path.splitext(file.filename)[1]}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.makedirs(app.config['UPLOAD_FOLDER'])
                file.save(file_path)
                new_file = PlayerImg(filename=filename, player=player)
                db.session.add(new_file)
                k=True
            if k == False:
                filename=f"placeholder{random.randint(1,4)}.png"
                new_file = PlayerImg(filename=filename, player=player)
                db.session.add(new_file)               
            db.session.add(player)
            db.session.commit()
        return redirect(url_for("index"))
@app.route("/next")
def next():
    user= current_user
  
    counter =user.counter+1

    players = Player.query.filter_by(user_id=user.id).all()
    print(counter,players)
    if counter+1>len(players):
        counter=0
    user.counter=counter
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Перевіряємо, чи існує користувач з таким логіном
        existing_user = User.query.filter_by(
            username=form.username.data
        ).first()
        if existing_user:
            flash("Користувач з таким ім'ям вже існує!", "danger")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        flash("Реєстрація пройшла успішно!", "success")
        login_user(user)
        return redirect(url_for("index"))

    return render_template("register.html", form=form)
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Успішний вхід!", "success")
            return redirect(url_for("index"))

        flash("Невірний логін або пароль", "danger")

    return render_template("login.html", form=form)


# Сторінка виходу
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/hpAdd",methods=["PATCH"])
def hpAdd():
    json=request.get_json()
    id = json["id"]
    hp = int(json["hp"])
    if id:
        player = Player.query.get(int(id))
        if player:
            player.hp = player.hp+hp
            db.session.commit()
    return {"code":200}
@app.route("/hpSubtract",methods=["PATCH"])
def hpSubtract():
    json=request.get_json()
    id = json["id"]
    hp = int(json["hp"])
    if id:
        player = Player.query.get(int(id))
        if player:
            player.hp = player.hp-hp
            db.session.commit()
    return {"code":200}
@app.route("/del",methods=["DELETE"])
def delete_player():
    json=request.get_json()
    idd = json["id"]

    if idd:
        player = Player.query.get(int(idd))
        if player:
            db.session.delete(player)
            db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
