from flask import Flask, render_template
from flask_socketio import SocketIO,emit
import time
from flask import request
import json


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'windroc-nwpc-project'

socketio = SocketIO(app)

@app.route('/')
def get_index_page():
    return 'index.html'

@app.route('/test', methods=['GET', 'POST'])
def get_hpc_llq_info():
    r = request
    hpc_llq_info_message = json.loads(request.form['message'])
    print ("Receive llq info:", hpc_llq_info_message)
    socketio.emit('send_llq_info', hpc_llq_info_message, namespace='/hpc')
    result = {
        'status': 'ok'
    }
    result=json.dump(result)
    return result



if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)