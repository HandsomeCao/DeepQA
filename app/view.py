from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask.json import JSONEncoder as BaseEncoder, jsonify
from flask._compat import text_type
import config
import json
import codecs
import sys
from tqdm import tqdm
from exts import db
from models import Question, User
# from speaklater import _LazyString
from decorators import login_required


result = None

def decode_result(result):
    for r in result:
        for k, v in r.items():
            if isinstance(v, str):
                v = v.decode('UTF-8', 'strict')
    return result
        

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        keyword = request.form.get('keyword')
        if keyword is not None:
            questions = Question.query.filter(Question.q_text.like(
            '%' + keyword + '%'))
            questions = [q.serialize for q in questions.all()]
            # session['questions'] = questions
            global result
            result = questions
            return redirect(url_for('list'))
        else:
            return redirect(url_for('index'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.username == username).first()
        if user:
            if user.verify_password(password):
                session['user_id'] = user.id
                return redirect(url_for('index'))
            else:
                flash('密码错误!')
                return redirect(url_for('login'))
        else:
            flash('该用户名不存在!')
            return redirect(url_for('login'))

@app.route('/list/', methods=['GET', 'POST'])
def list():
    if request.method == 'GET':
        global result
        # paginate
        page = request.args.get('page', 1, type=int)
        # pagination = 
        return render_template('list.html', questions=result)
    else:
        keyword = request.form.get('keyword')
        questions = Question.query.filter(Question.q_text.like(
            '%' + keyword + '%'))
        questions = [q.serialize for q in questions.all()]
        global result
        result = questions
        return redirect(url_for('list'))


@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter(User.username == username).first()
        if user:
            flash('该用户名已经被注册!')
            return redirect(url_for('regist'))
        else:
            if password1 != password2:
                flash('两次输入的密码不相等!')
                return redirect(url_for('regist'))
            else:
                user = User(username=username, password=password1)
                db.session.add(user)
                db.session.commit()
                flash('注册成功!')
                return redirect(url_for('login'))

@app.route('/history/', methods=['GET', 'POST'])
@login_required
def history():
    pass



# JSON_PATH = './notebooks/ai_challenger_oqmrc_trainingset.json'
# insert pre-data to the database from training and valid json file

# @app.route('/insert_data')
# def insert_data():
#     with open(JSON_PATH, 'r', encoding='utf-8') as f:
#         for line in tqdm(f.readlines()):
#             dic = json.loads(line, encoding='utf-8')
#             q_text = dic['query']
#             p_text = dic['passage']
#             alternatives = dic['alternatives']
#             dataset = 'train'
#             question = Question(q_text=q_text, p_text=p_text, 
#                 alternatives=alternatives, dataset=dataset)
#             db.session.add(question)
#     db.session.commit()
#     return 'Done'
