# 1. Use an official Python image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy your requirements file first (Efficiency trick!)
COPY requirements.txt .

# 4. Install the libraries
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /app/data


# 5. Copy your python script into the container
COPY weather_extractor.py .

# 6. The command to run your script
CMD ["python", "weather_extractor.py"]