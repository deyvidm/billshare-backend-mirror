FROM python:3
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app/
EXPOSE 3000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:3000"]