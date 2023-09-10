# Use a Python 3.7 image
FROM python:3.11

# Copy the current directory contents into the container at /app
COPY ./app /var/www/app
COPY ./requirements.txt /var/www/requirements.txt

WORKDIR /var/www

VOLUME ["/var/www/app/uploads"]

# Install npm
RUN apt update
RUN apt-get install -y nodejs npm

# Upgrade Pip and Install Requirements
RUN python -m pip install -r requirements.txt

# Install Javascript Packages
WORKDIR /var/www/app/static
RUN npm install

WORKDIR /var/www

# Run the production version of the web app
CMD python -m gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:5000 app:app
EXPOSE 5000
