FROM python:3.12.6

WORKDIR /app

COPY . /app

# Copy the requirements file and install dependencies
COPY requirements.txt .

# Install the dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]