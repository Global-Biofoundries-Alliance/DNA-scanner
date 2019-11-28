FROM alpine:3.1

# Update 
RUN apk add --update python py-pip

# Copy Python Sources
WORKDIR /src/backend/
COPY Controller .
COPY Pinger .
ADD *.py .

# Copy Konfiguration File
ADD config.yml .
ADD requirements.txt .

# Install app dependencies
RUN pip install -r requirements.txt

# Expose Port
EXPOSE 8080

# Run Python-Application
CMD ["python", "/src/backend/"]
