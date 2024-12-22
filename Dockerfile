# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /src

# Copy the current directory contents into the container at /app
COPY . /src

# Copy the entrypoint script and ensure it's executable
COPY ./entrypoint.sh /entrypoint.sh
# Copy the entrypoint script and ensure it's executable
RUN chmod +x /entrypoint.sh

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements/staging.txt

# Expose the Flask app's port
EXPOSE 5000

# Define the default entrypoint for the container
ENTRYPOINT ["entrypoint.sh"]
