FROM python

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

RUN chmod a+x docker/*.sh

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]