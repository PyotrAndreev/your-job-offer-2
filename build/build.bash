#! /bin/bash

# Build Assumptions:
# Python3 and pip3 are installed properly
python3 -m venv venv
source venv/bin/activate
sudo apt install build-essential libpoppler-cpp-dev pkg-config python3-dev # для pdftotext
mkdir -p your_job_offer/logs
pip3 install -r build/requirements.txt
pip3 install -r build/requirements-dev.txt
pip3 install -e .
export $(grep -v '^#' secrets/.env | xargs)
SERVICE_NAME="db"
if [ -z "$(docker ps -q -f name=${SERVICE_NAME})" ]; then
    docker-compose up -d
else
    echo "Контейнер '${SERVICE_NAME}' уже запущен."
fi