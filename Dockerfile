# lambda supported docker image
FROM public.ecr.aws/lambda/python:3.9 AS builder

# install required packages
COPY requirements.txt ./
RUN pip install -r ./requirements.txt

# copy app to docker
COPY src/main.py ./
COPY src/explain_fallacy.py ./

# this is the image entrypoint
CMD ["main.lambda_handler"]