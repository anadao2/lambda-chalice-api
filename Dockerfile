FROM python:3.9-slim
WORKDIR /app
COPY . . 

# Install default services
RUN pip install -r requirements.txt
CMD ./entrypoint.sh