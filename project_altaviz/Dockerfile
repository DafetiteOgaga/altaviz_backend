# Step 1: Use an official Node.js (for react)/Python (for django) image
FROM python:3.10

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements file to the container
COPY requirements.txt .

# Step 4: Install dependencies
RUN pip install -r requirements.txt

# Step 5: Copy the rest of the app's code to the container
COPY . .

# Step 6: Expose port 8000 (Django's default port)
EXPOSE 8000

# Step 7: Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

