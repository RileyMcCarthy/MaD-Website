from flask import Flask
from flask_socketio import SocketIO

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'gcode', 'nc', 'txt'}



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROFILE_FOLDER'] = UPLOAD_FOLDER + '/profiles'
app.config['TEST_FOLDER'] = UPLOAD_FOLDER + '/tests'
socketio = SocketIO(app, async_mode='threading')

from app import base, status, settings, upload, data, create
from app.base import serial_thread, state_thread, data_thread, test_data_reciever_thread, emit_notification