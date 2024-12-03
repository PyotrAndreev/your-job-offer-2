FROM python:3.9-slim-buster
WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apt-get update && apt-get -y install libpq-dev gcc && pip install psycopg2
COPY build/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
COPY your_job_offer ./your_job_offer
CMD ["python", "your_job_offer/app.py"]