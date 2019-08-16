from flask import Flask, request, send_file, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
import io
import uuid

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

db = SQLAlchemy(app)

class Patrimonio(db.Model):
    __tablename__ = "patrimonio"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))   
    tag_id = db.Column(db.String(255), unique=True)
    latitude = db.Column(db.String(255))
    longitude = db.Column(db.String(255))
    img_path = db.Column(db.String(225))

    def __init__(self, nome, tag_id, latitude, longitude, img_path):
        self.nome = nome  
        self.tag_id = tag_id
        self.latitude = latitude
        self.longitude = longitude
        self.img_path = img_path

    def to_json(self):
        return {'nome': self.nome,
                'tag_id': self.tag_id,
                'latitude': self.latitude,
                'longitude': self.longitude,
                'img_path': self.img_path}

@app.route('/patrimonio/adicionar', methods=['POST'])
def adicionar_patrimonio():

    p = Patrimonio(
        request.json['nome'],
        request.json['tag_id'],
        request.json['latitude'],
        request.json['longitude'],
        request.json['img_path'],
    )

    db.session.add(p)
    db.session.commit()
    return 'ok'

@app.route('/patrimonio/apagar', methods=['GET'])
def apagar_patrimonio():
    
    for p in Patrimonio.query.all():
        db.session.delete(p)
    db.session.commit()

    return 'apagado!'

@app.route('/patrimonio/<tag_id>', methods=['GET'])
def get_patrimonio(tag_id):
    patrimonio = Patrimonio.query.filter_by(tag_id=tag_id).first()
    
    return patrimonio.to_json()

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['file']
    filename = gen_unique_file_name()
    check_dir_exists()
    file.save('./static/' + filename + '.jpg')

    return filename

def check_dir_exists():
    if not os.path.exists('./static/'):
        os.makedirs('./static/')
        print(os.path.dirname(os.path.abspath(__file__)))

def gen_unique_file_name():
    return str(uuid.uuid4())

@app.route('/img/<path:filename>') 
def send_file(filename): 
    return send_from_directory('./static/', filename)

if __name__ == '__main__':
    app.run()