from app import app, socketio, ALLOWED_EXTENSIONS
from flask import render_template, request, jsonify, Response, flash, redirect, url_for
from .base import gcode_sender_thread, gcode_to_dict, emit_notification, generate_gcode_from_profile
import app.communication as communication
import os
import numpy as np
from io import StringIO
import sys
import contextlib
import json

@app.route('/upload', methods=['GET'])
def upload_page():
    files = os.listdir(app.config['PROFILE_FOLDER'])
    return render_template('upload.html', files=files)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        emit_notification('error', 'No file found in request!')
        return redirect(url_for('upload_page'))

    file = request.files['file']
    filename = request.form['filename']

    if not filename.endswith('.gcode'):
        filename += '.gcode'
    if file and filename:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        emit_notification('success', 'File uploaded successfully!')
    else:
        emit_notification('error', 'No file selected!')
    return redirect(url_for('upload_page'))

@app.route('/select', methods=['POST'])
def select():
    selected_file = request.form['selected_file']
    path = os.path.join(app.config['PROFILE_FOLDER'], selected_file)
    socketio.start_background_task(target=gcode_sender_thread, filename=path)
    return f"Sending {selected_file} file to machine"

@app.route('/gcode_file_to_moves', methods=['POST'])
def gcode_file_to_moves():
    selected_file_json = request.get_json()
    selected_file = selected_file_json['filename']
    path = os.path.join(app.config['PROFILE_FOLDER'], selected_file)
    gcode_str = generate_gcode_from_profile(path)
    print(gcode_str)
    cordinates = []
    last_position = 0
    time = 0
    for line in gcode_str.splitlines():
        command = gcode_to_dict(line)
        if command is None:
            continue
        if command['G'] == 4:
            position = last_position
            time += command['P']/1000.0
        elif command['G'] == 0 or command['G'] == 1:
            position = command['X'] # mm
            feedrate = command['F'] # mm/min
            if feedrate != 0:
                time += abs(position-last_position)/(feedrate/60)
        elif command['G'] == 122:
            break # end of gcode file
        else:
            continue # Skip unknown gcode commands
        cord = {"X": time, "Y": position}
        cordinates.append(cord)
        last_position = position
    return json.dumps(cordinates)

@app.route('/jog', methods=['POST'])
def jog_machine():
    g = int(request.form['g'])
    x = float(request.form['x'])
    f = float(request.form['f'])
    command = {'G': g, 'X': x, 'F': f}
    print(command)
    communication.set_manual_command(command)
    return redirect(url_for('upload_page'))
