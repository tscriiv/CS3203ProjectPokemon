FROM python:3



COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY src/app.py ./


EXPOSE 5000


CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]

