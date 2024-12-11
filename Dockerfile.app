FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get -y install libpq-dev gcc
COPY pyproject.toml build/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY your_job_offer ./your_job_offer
RUN pip install --no-cache-dir -e .

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 8080
CMD ["python3","-u", "your_job_offer/app.py", "--host=0.0.0.0"]
