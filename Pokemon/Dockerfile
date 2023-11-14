
FROM python:latest

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY src/app.py ./
COPY src/templates/ /templates/
COPY src/static/ /static/

CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]

