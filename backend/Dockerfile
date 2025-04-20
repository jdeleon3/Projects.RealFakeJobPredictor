FROM public.ecr.aws/lambda/python:3.11

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Add app
COPY app/ ./app/

# Set FastAPI as Lambda handler
CMD ["app.main.handler"]