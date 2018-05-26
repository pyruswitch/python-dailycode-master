__author__ = 'vincent'
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>1234</h1>'

@app.route('/signin', methods=['GET'])
def signin_form():
    return '''1234'''

@app.route('/signin', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    return '1234'


if __name__ == '__main__':
    app.run()