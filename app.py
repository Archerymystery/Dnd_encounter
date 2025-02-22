from flask import Flask, render_template,request,redirect,url_for
from config import Config
from models import db, Player,PlayerImg
import random
import os
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
counter = 0
with app.app_context():
    db.create_all()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
@app.route("/")
def index():
    players = Player.query.order_by(Player.init.desc()).all()
    
    selected = request.args.get('selected')
    if selected is None:
        selectedPlayer = players[counter]
    else:
        selectedPlayer = Player.query.get(int(selected))
    return render_template("index.html",selected=selectedPlayer,counter=players[counter],players=players)
@app.route("/add", methods=["POST","GET"])
def add_player():
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
            player = Player(name=name,speed=speed,hp_max=hp_max,hp=hp_max,init=initative,ac=ac,lv=level)
            files = request.files.getlist("img")
            k=False
            for file in files:
                if file and allowed_file(file.filename):
                    filename=f"{player.id}.{ os.path.splitext(file.filename)[1]}"
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    if not os.path.exists(app.config['UPLOAD_FOLDER']):
                        os.makedirs(app.config['UPLOAD_FOLDER'])
                    file.save(file_path)
                    new_file = PlayerImg(filename=filename, player_img_id=player)
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
    global counter
    counter +=1
    players = Player.query.all()
    if counter+1>len(players):
        counter=0
    return redirect(url_for("index"))
if __name__ == "__main__":
    app.run(debug=True)