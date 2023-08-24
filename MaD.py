from app import app, socketio, serial_thread, state_thread, data_thread
import subprocess
import logging
@app.route("/restart")
def restart():
    subprocess.run("shutdown -r 0", shell=True, check=True)
    return "Restarting"

@app.route("/shutdown")
def shutdown():
    subprocess.run("shutdown -h 0", shell=True, check=True)
    return "Shutting down!"

if __name__ == "__main__":
    try:
        socketio.run(app,
                        port=5000,
                        host="0.0.0.0")
    except KeyboardInterrupt:
        pass
