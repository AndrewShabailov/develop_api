FROM mcr.microsoft.com/playwright/python:latest

ARG TEST_PROFILE=api
ARG BACKEND_URL=http://host.docker.internal:4111/api

ENV TEST_PROFILE=${TEST_PROFILE}
ENV BACKEND_URL=${BACKEND_URL}

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["pytest", "-m", "api", "--alluredir=/app/reports/allure"]