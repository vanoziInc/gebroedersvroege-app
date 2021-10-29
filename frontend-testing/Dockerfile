FROM mcr.microsoft.com/playwright:focal
WORKDIR /root

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["pytest"]
