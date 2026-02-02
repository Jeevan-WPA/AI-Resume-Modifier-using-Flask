# Use the official Playwright Python image which includes browsers and system dependencies
FROM mcr.microsoft.com/playwright/python:v1.49.0-jammy

# Prevent Python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies for LaTeX to PDF conversion
# texlive-latex-extra includes many common packages used in resume templates
# latexmk is required by the python dependency 'latexmk'
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-fonts-recommended \
    texlive-latex-extra \
    latexmk \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers (if not fully covered by the base image, though usually they are)
RUN playwright install

# Copy project files
COPY . .

# Create directory for database/outputs if they don't exist
RUN mkdir -p output

# Expose port 5000 for Flask
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
