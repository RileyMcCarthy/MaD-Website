FROM python:slim-bullseye

# Copy the current directory contents into the container at /app
COPY ./app /var/www/app
COPY ./requirements.txt /var/www/requirements.txt

WORKDIR /var/www

VOLUME ["/var/www/app/uploads"]

# Pre-requisites for opencv
RUN apt update && apt install -y libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx

# Install npm
RUN apt-get update && apt-get install -y nodejs npm

# Create Python Venv and Install Requirements
RUN python3 -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt

# Install Javascript Packages
WORKDIR /var/www/app/static
RUN npm install

WORKDIR /var/www

# Run the production version of the web app
CMD venv/bin/gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:5000 app:app
EXPOSE 5000
