FROM python:3.9.13

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]