FROM mcr.microsoft.com/playwright:focal
WORKDIR /root

COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN playwright install
COPY . .

ENTRYPOINT ["DEBUG=pw:api pytest -s"]