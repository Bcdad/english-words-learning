from wtforms import Form, StringField
from wtforms.validators import length, email, equal_to


class RegisterForm(Form):
    Username = StringField(validators=[length(min=3, max=20, message="请输入正确的用户名！")])
    # email=StringField(validators=[email(message='请输入正确的邮箱')])
    Password = StringField(validators=[length(min=6, max=20, message="请输入正确的密码！")])
    confirm_password = StringField(validators=[equal_to('Password', message='两次密码不一致')])


class RegisterForms(Form):
    Username = StringField(validators=[length(min=3, max=20, message="请输入正确的用户名！")])
    # email=StringField(validators=[email(message='请输入正确的邮箱')])
    Password = StringField(validators=[length(min=6, max=20, message="请输入正确的密码！")])
    # confirm_password = StringField(validators=[equal_to('Password', message='两次密码不一致')])
