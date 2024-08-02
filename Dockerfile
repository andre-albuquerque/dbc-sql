FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install mysql client
RUN apt-get update && apt-get install -y mariadb-client

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Keep the container running
CMD ["tail", "-f", "/dev/null"]