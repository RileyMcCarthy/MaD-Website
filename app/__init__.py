from flask import Flask
from flask_socketio import SocketIO
import os
import logging
import configparser

UPLOAD_FOLDER = './app/uploads'
ALLOWED_EXTENSIONS = {'gcode', 'nc', 'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROFILE_FOLDER'] = UPLOAD_FOLDER + '/profiles'
app.config['TEST_FOLDER'] = UPLOAD_FOLDER + '/tests'
os.makedirs(app.config['PROFILE_FOLDER'], exist_ok=True)
os.makedirs(app.config['TEST_FOLDER'], exist_ok=True)
logging.basicConfig(filename='error.log',level=logging.DEBUG)
socketio = SocketIO(app)

from app import base, status, settings, upload, data, create
from app.base import serial_thread, test_data_reciever_thread, emit_notification


serial_thread_ref = socketio.start_background_task(serial_thread)