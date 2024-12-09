FROM python:3.12-slim
WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apt-get update && apt-get -y install libpq-dev gcc && pip install psycopg2
COPY build/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
COPY your_job_offer ./your_job_offer
CMD ["python3","-u", "your_job_offer/app.py", "--host=0.0.0.0"]
