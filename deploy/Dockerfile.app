FROM base

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 8080
CMD ["python3","-u", "your_job_offer/app.py", "--host=0.0.0.0"]
