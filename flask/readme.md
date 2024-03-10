# 英语单词4,6级系统  

## api分析  

```python
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
```

这个 API 接口是一个 POST 请求，它接收一个 JSON 对象作为输入，该对象包含以下字段：

>word：字符串类型 需要翻译的单词或句子。  
>choice：字符串类型 用户的选择，但在这段代码中并未使用。  
>hold：布尔类型 一个标志，表示是否需要保存这个单词。  
>username：字符串类型 用户的名称。  
>最后，这个接口返回一个 JSON 对象，包含了单词的中文翻译、英文原文、两个例句和音标。  
>chinese 字符串类型  
>english 字符串类型  
>sentence1 字符串类型  
>sentence2 字符串类型  
>phonetic 字符串类型  

```python
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
```

Sign API
POST /sign
用于注册新用户。  
  
请求体  
请求体应为一个JSON对象，包含以下字段：  

pass1：字符串，用户的密码。  
pass2：字符串，用户再次输入的密码，用于确认。  
account：字符串，用户的账号。  
响应  
响应体为一个JSON对象，包含以下字段：  

pass3：字符串，如果pass1和pass2相等，则为'yes'，否则为'no'。  
pass4：字符串，如果账号长度在3到20个字符之间，且密码长度在6到20个字符之间，则为'yes'，否则为'no'。  
pass5：字符串，如果账号已存在，则为'no'，否则为'yes'。  
如果pass3、pass4和pass5都为'yes'，则会创建新的用户，并将其添加到数据库。  

```python
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
```

Study API  
POST /study  
用于获取指定用户的学习数据。  

请求体  
请求体应为一个JSON对象，包含以下字段：  

user：字符串，用户的账号。  
响应
响应体为一个JSON对象，包含一个content字段，其值为一个对象数组。每个对象代表一条学习数据，包含以下字段：  

id：整数，数据的唯一标识符。  
user：字符串，用户的账号。  
eng：字符串，英文数据。  
sen1：字符串，句子1。  
sen2：字符串，句子2。  
pho：字符串，音标。  
chn：字符串，中文数据。  

```python
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
            q = requests.post('http://127.0.0.1:8080/api/v1.0', json={'word': eng},
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
```

Num API
POST /num
用于获取指定数量的新学习数据，并将其添加到指定用户的学习数据中。  

请求体
请求体应为一个JSON对象，包含以下字段：  

num：整数，需要获取的新学习数据的数量。  
user：字符串，用户的账号。  
响应  
响应体为一个JSON对象，包含一个content字段，其值为一个对象数组。每个对象代表一条新的学习数据，包含以下字段：  
  
english：字符串，英文数据。  
chinese：字符串，中文数据。  
sentence1：字符串，句子1。  
sentence2：字符串，句子2。  
phonetic：字符串，音标。  

```python
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
```

POST /login1
用于验证用户的用户名和密码。

请求体
请求体应为一个JSON对象，包含以下字段：

username：字符串，用户的账号。  
password：字符串，用户的密码。  
响应  
响应体为一个JSON对象，包含一个username字段，其值为一个布尔值。如果用户名和密码正确，则为true，否则为false。  
  
## 项目说明

>本项目前端使用vue进行开发，后端使用flask进行开发
>实现了账号的登录，单词的查询，学习以及数据的保存等功能  
>其中翻译功能调用了百度的翻译接口，例句，音标等功能调用了freedictionary的接口  
>使用了mysql数据库，运行于3306端口，用户名为root，密码123456，信息存储于login数据库中，里面有三张表  

### dates  

>id 整数 主键  
>user 字符串 用户名  
>eng 字符串 单词英文  
>chn 字符串 单词中文  
>sen1 字符串 例句一  
>sen2 字符串 例句二  
>pho  字符串 音标  

### user  

>id 整数 主键  
>username 字符串 用户名  
>password 字符串 密码  
>study_date int 用于快速定位学习数据，对应words表主键  

### words

>id 整数 主键  
>eng 英文  
>chn 中文  

## 路由说明

|路由|对应界面|插件|
|:-:|:-:|:-:|
|'/'                |登录界面        |HomeView.vue  |
|'/signup'          |注册界面        |signup.vue  |
|'/study/:username' |单词学习界面    |study.vue  |
|'/user/:username'  |翻译界面        |user.vue  |
|'/data/:username'  |学习数据界面     |data.vue  |
