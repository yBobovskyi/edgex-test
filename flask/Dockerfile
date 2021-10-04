FROM python:3.7-alpine
WORKDIR /app
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install flask redis
EXPOSE 5000
COPY . .
CMD ["flask", "run"]