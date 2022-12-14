from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, TEXT, INTEGER
from flask import Response
import json

from dotenv import load_dotenv
import os

load_dotenv()
DB = os.environ.get("DB")
DB_USER = os.environ.get("DB_USER")
DB_PW = os.environ.get("DB_PASSWORD")
DB_ENDPOINT = os.environ.get("DB_HOST")
sql_uri = "{}://{}:{}@{}".format(DB,DB_USER,DB_PW,DB_ENDPOINT)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = sql_uri
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
db = SQLAlchemy(app)


class Answer(db.Model):
    __tablename__ = "answer_list"

    id = Column(INTEGER, autoincrement=True, primary_key=True)
    form_id = Column(TEXT)
    name = Column(TEXT)
    answers = Column(TEXT)

def get_data_from_postgresql():
        
    rows = Answer.query.all()
    
    rows.sort(key=lambda x:x.name)
    
    excepts = ['Wl074O', 'W2vX3J', 'RZ96pb', 'W7ADn2', 'ML8wOq', 'Wo8Ym1']
    
    result = [{
        'id': idx+1,
        'name': row.name.split(' ')[0],
        'answers': row.answers
    } for idx, row in enumerate(rows) if row.form_id not in excepts]
    
    result = [{
        'id': idx+1,
        'name': row['name'],
        'answers': row['answers']
    } for idx, row in enumerate(result)]

    return result 

@app.route('/api/data')
def get_qustion_data():
    
    data_list = get_data_from_postgresql()
    res = json.dumps(data_list,ensure_ascii=False).encode('utf8')  
    r = Response(response=res, status=200, content_type='application/json; charset=utf-8')
    r.headers["Access-Control-Allow-Origin"]="*"
    return r

@app.route('/api/home')
def default():

    return {"hi":"hello"}

if __name__ == '__main__':
    app.run(host='0.0.0.0')