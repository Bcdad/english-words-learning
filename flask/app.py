from flask import Flask, render_template, url_for, redirect, request, flash, jsonify
from forms import RegisterForm, RegisterForms
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
import pymysql
import requests
from googletrans import Translator
import re
import json
import hashlib
from flask_cors import CORS

translator = Translator(service_urls=[
    'translate.google.com',
    'translate.google.co.kr',
])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ADFHJIOibuQ'
app.app_context().push()
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/login'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)


# 定义Api
class Translate(Resource):
    def post(self):
        data = request.json
        word = data.get('word')
        choice = data.get('choice')
        hold = data.get('hold')
        username = data.get('username')
        if re.compile('[a-zA-Z]+').findall(word):
            sign = hashlib.md5(f"20231005001837619{word}123oAfqxxI6rt00jTYwLg6R".encode()).hexdigest()
            response = requests.post(
                f'http://api.fanyi.baidu.com/api/trans/vip/translate?q={word}&from=en&to=zh&appid=20231005001837619&salt=123&sign={sign}')
            chinese = response.json()['trans_result'][0]['dst']
            english = word
        else:
            sign = sign = hashlib.md5(f"20231005001837619{word}123oAfqxxI6rt00jTYwLg6R".encode()).hexdigest()
            response = requests.post(
                f'http://api.fanyi.baidu.com/api/trans/vip/translate?q={word}&from=zh&to=en&appid=20231005001837619&salt=123&sign={sign}')
            english = response.json()['trans_result'][0]['dst']
            chinese = word

        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{english}")
        _data = response.json()
        try:
            phonetic = _data[0]['phonetic']
        except:
            try:
                phonetic = _data[0]['phonetics'][1]['text']
            except:
                phonetic = '暂时无法查询到'
        try:
            sen = []
            new = [obj['definitions'] if 'definitions' in obj else None for obj in _data[0]['meanings']]
            for de in new:
                for i in range(len(de)):
                    if 'example' in de[i]:
                        sen.append(de[i]['example'])
            if len(sen) == 1:
                sentence1 = sen[0]
                sentence2 = '暂无数据'
            else:
                sentence1 = sen[0]
                sentence2 = sen[1]
        except:
            sentence2 = '暂无数据'
            sentence1 = '暂无数据'
        if hold == 'yes' and not Data.query.filter_by(eng=english, user=username).first():
            data_ = Data(user=username, eng=english, chn=chinese, sen1=sentence1, sen2=sentence2, pho=phonetic)
            db.session.add(data_)
            db.session.commit()
            print('true')

        return jsonify({
            'chinese': chinese,
            'english': english,
            'sentence1': sentence1,
            'sentence2': sentence2,
            'phonetic': phonetic
        })


class Sign(Resource):
    def post(self):
        data = request.json
        pass1 = data.get('pass1')
        pass2 = data.get('pass2')
        account = data.get('account')
        if pass1 == pass2:
            pass3 = 'yes'
        else:
            pass3 = 'no'
        if len(account) > 20 or len(account) < 3 or len(pass2) < 6 or len(pass2) > 20:
            pass4 = 'no'
        else:
            pass4 = 'yes'
        if User.query.filter_by(username=account).first():
            pass5 = 'no'
        else:
            pass5 = 'yes'
        if pass4 == 'yes' and pass3 == 'yes' and pass5 == 'yes':
            user = User(username=account, password=pass1)
            db.session.add(user)
            db.session.commit()
        return jsonify({
            'pass3': pass3,
            'pass4': pass4,
            'pass5': pass5
        })


class Study(Resource):
    def post(self):
        user = request.json.get('user')
        study_data = Data.query.filter_by(user=user).all()
        print(study_data)
        # return jsonify({
        #     'content':study_data
        # })
        study_data_dict = [
            {'id': item.id, 'user': item.user, 'eng': item.eng, 'sen1': item.sen1, 'sen2': item.sen2, 'pho': item.pho,
             'chn': item.chn}
            for
            item in study_data]
        # study_data_dict = [item.as_dict() for item in study_data]
        return jsonify({'content': study_data_dict})


class Num(Resource):
    def post(self):
        num = int(request.json.get('num'))
        user = request.json.get('user')
        study_user = User.query.filter_by(username=user).first()
        _study_data = study_user.study_data

        def new(num):
            if Data.query.filter_by(user=user, eng=Word.query.filter_by(id=num).first().eng).first():
                return new(num + 1)
            else:
                return num

        datas = []
        for a in range(num):
            eng = Word.query.filter_by(id=new(_study_data)).first().eng
            q = requests.post('http://127.0.0.1:81/api/v1.0', json={'word': eng},
                              headers={'Content-Type': 'application/json'}).json()
            data=Data(user=user, eng=q['english'], chn=q['chinese'], sen1=q['sentence1'], sen2=q['sentence2'], pho=q['phonetic'])
            db.session.add(data)
            db.session.commit()
            _study_data = new(_study_data)
            datas.append(q)
        study_user.study_data = _study_data
        db.session.commit()
        return jsonify({
            'content': datas
        })

class Login1(Resource):
    def post(self):
        if User.query.filter_by(username=request.json.get('username'), password=request.json.get('password')).first():
            return jsonify({
                'username': True
            })
        else:
            return jsonify({
                'username': False
            })




api.add_resource(Num, '/api/v1.0/study')

api.add_resource(Study, '/api/v3.0')

api.add_resource(Sign, '/api/v2.0')

api.add_resource(Translate, '/api/v1.0')

api.add_resource(Login1,'/api/login')


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    study_data = db.Column(db.Integer, default=1)


class Data(db.Model):
    __tablename__ = 'datas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(100))
    eng = db.Column(db.String(100))
    chn = db.Column(db.String(100))
    pho = db.Column(db.String(100))
    sen1 = db.Column(db.String(100))
    sen2 = db.Column(db.String(100))


class Word(db.Model):
    __tablename__ = 'words'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    eng = db.Column(db.String(100))
    chn = db.Column(db.String(100))


db.create_all()
db.session.commit()


# class Haxi(db.Model):
#     __tablename__ = 'haxi'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     ha = db.Column(db.String(100))


# class Login(Resource):
#     def get(self):
#         return render_template('login.html')
#     def post(self):
#         form = RegisterForms(request.form)
#         if form.validate():
#             if User.query.filter_by(username=form.Username.data, password=form.Username.data):
#                 return app.send_static_file('login.html')
#             else:
#                 flash('账号或密码错误')
#                 return redirect(url_for('login'))
#
# api.add_resource(Login,'/')
# 登录界面
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = RegisterForms(request.form)
        if form.validate():
            if User.query.filter_by(username=form.Username.data, password=form.Password.data).first():
                return redirect(f'/translate/{form.Username.data}')
            else:
                flash('账号或密码错误')
                return redirect(url_for('login'))
            # hash1=Haxi.query.filter_by(ha=index).first()
            # if hash1:
            #     return render_template('rain.html')
            #
            #     return render_template(url_for('login'))
        # if form.validate():
        #     user = User.query.filter_by(username=form.Username.data).first()
        #     if user and user.password == form.Password.data:
        #         return render_template('rain.html')
        #     else:
        #         return redirect('/')
        # if form.validate():
        #     if form['Username'].data == 'xin' and form['Password'].data == '123456':
        #         return render_template('rain.html')
        #     else:
        #         flash(form['Username'])
        #         flash(form['Password'])
        #         flash(form['Username'] == 'xin' and form['Password'] == '123456')
        #         return redirect('/')
        else:
            for errors in form.errors.values():
                for error in errors:
                    flash(error)
            return redirect(url_for('login'))


# 忘记界面
@app.route('/forget')
def forgot():
    return render_template('forget.html')


# 注册界面
@app.route('/sign', methods=['GET'])
def sign_up():
    return render_template('signup.html')
    # if request.method == 'GET':
    #     return render_template('signup.html')
    # else:
    #     form = RegisterForm(request.form)
    #     if form.validate():
    #         user = User(username=form.Username.data, password=form.Password.data)
    #         if User.query.filter_by(password=form.Username.data):
    #             flash("该账号已存在")
    #             return redirect(url_for('sign_up'))
    #
    #         else:
    #             class English(db.Model):
    #                 __tablename__ = 'id' + str(user.id)
    #                 id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    #                 word = db.Column(db.String(100))
    #
    #             db.create_all()
    #             db.session.add(user)
    #             db.session.commit()
    #             return redirect('/')
    #     else:
    #         for errors in form.errors.values():
    #             for error in errors:
    #                 flash(error)
    #         return redirect(url_for('sign_up'))


@app.route('/translate/<username>', methods=['GET', 'POST'])
def _translate(username):
    return render_template('form.html', username=username)


@app.route('/data/<user>', methods=['GET'])
def _data(user):
    return render_template('data.html', user=user)


@app.route('/study/<user>')
def _num(user):
    return render_template('study.html', user=user)


if __name__ == '__main__':
    app.run()
