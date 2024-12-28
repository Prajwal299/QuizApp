FROM python:3.11.3

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 5000 (used by Flask by default)
EXPOSE 5000

# Specify the entrypoint
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
