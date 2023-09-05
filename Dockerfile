FROM python:3.11

# Copy the current directory contents into the container at /app
COPY ./app /var/www/app
COPY ./requirements.txt /var/www/requirements.txt

WORKDIR /var/www

VOLUME ["/var/www/app/uploads"]

# Pre-requisites for opencv
RUN apt update && apt install -y libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx

# Install npm
RUN apt-get update && apt-get install -y nodejs npm

# Install OpenCV
RUN apt-get update && apt-get -y install cmake protobuf-compiler
RUN apt-get install -y python3-opencv

# Upgrade Pip and Install Requirements
RUN python3 -m ensurepip --upgrade
RUN python3 -m pip install --upgrade pip setuptools wheel
RUN python3 -m pip install -r requirements.txt

# Install Javascript Packages
WORKDIR /var/www/app/static
RUN npm install

WORKDIR /var/www

# Run the production version of the web app
CMD python3 -m gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:5000 app:app
EXPOSE 5000
