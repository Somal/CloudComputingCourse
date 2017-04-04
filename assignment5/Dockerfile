FROM django:1.10-python3
RUN apt-get -y update
RUN apt-get -y install git
ADD ./ app/
WORKDIR app
EXPOSE 8000
CMD python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000