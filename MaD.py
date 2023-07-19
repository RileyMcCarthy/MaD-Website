from app import app, socketio, serial_thread, state_thread, data_thread
import subprocess
import configparser

@app.route("/restart")
def restart():
    subprocess.run("shutdown -r 0", shell=True, check=True)
    return "Restarting"

@app.route("/shutdown")
def shutdown():
    subprocess.run("shutdown -h 0", shell=True, check=True)
    return "Shutting down!"

if __name__ == "__main__":
    serial_port = "/dev/serial0"
    serial_baud=9600
    server_port = 5001
    config = configparser.ConfigParser()
    config.read('config.ini')
    if "SERVER_PORT" in config['DEFAULT']:
        server_port = config['DEFAULT']['SERVER_PORT']
    if "SERIAL_PORT" in config['DEFAULT']:
        serial_port = config['DEFAULT']['SERIAL_PORT']
    if "SERIAL_BAUD" in config['DEFAULT']:
        serial_baud = config['DEFAULT']['SERIAL_BAUD']
    try:
        socketio.start_background_task(serial_thread, serial_port, serial_baud)
        socketio.start_background_task(state_thread)
        socketio.start_background_task(target=data_thread)
        socketio.run(app,
                     port=server_port,
                     host="0.0.0.0",
                     debug=True,
                     use_reloader=False)
    except KeyboardInterrupt:
        pass
