FROM python:3.10-alpine
LABEL version=1.0
RUN mkdir -p home/app
WORKDIR /app
COPY . /app
#RUN chown -R root /app
#RUN chmod 700 /app
RUN python3 -m venv venv
RUN source .venv/bin/activate
RUN pip install -r requirements.txt
CMD python app.py