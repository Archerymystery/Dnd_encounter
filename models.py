from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    ac = db.Column(db.Integer,nullable=False)
    speed = db.Column(db.Integer,nullable=False)
    init = db.Column(db.Integer,nullable=False)
    hp_max = db.Column(db.Integer,nullable=False)
    hp = db.Column(db.Integer,nullable=False)
    lv=db.Column(db.Integer,nullable=False)
    files = db.relationship('PlayerImg', backref='player', lazy=True, cascade="all, delete")
    
    # def __repr__(self):
    #     return f"<Task {self.title}>"


class PlayerImg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    player_img_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
