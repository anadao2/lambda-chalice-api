FROM python:3.14.0rc1-slim
WORKDIR /app
COPY . . 

# Install default services
RUN pip install -r requirements.txt
CMD ./entrypoint.sh