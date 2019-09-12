FROM gcr.io/google-appengine/python
RUN apt-get update
RUN apt-get install -y xvfb
RUN apt-get install -y firefox
LABEL python_version=python
RUN virtualenv --no-download /env -p python
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app/
CMD exec gunicorn -b :$PORT main:app --timeout 180