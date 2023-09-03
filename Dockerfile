FROM python:3.11

# Copy the current directory contents into the container at /app
COPY ./app /var/www/app
COPY ./requirements.txt /var/www/requirements.txt

WORKDIR /var/www

VOLUME ["/var/www/app/uploads"]

# Pre-requisites for opencv
RUN apt update && apt install -y libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx

# Install npm
RUN apt-get update && apt-get install -y nodejs npm protobuf-compiler
RUN apt-get install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 python3-pyqt5 python3-dev -y
RUN apt-get install python-opencv
# Create Python Venv and Install Requirements
RUN python3 -m venv venv
RUN venv/bin/python -m ensurepip --upgrade
RUN venv/bin/pip install --upgrade pip setuptools wheel
RUN venv/bin/pip install -r requirements.txt

# Install Javascript Packages
WORKDIR /var/www/app/static
RUN npm install

WORKDIR /var/www

# Run the production version of the web app
CMD venv/bin/gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:5000 app:app
EXPOSE 5000
