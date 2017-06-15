FROM python:3.6.1
ENV PYTHONUNBUFFERED 1

RUN echo "bust cache <increment me>" && mkdir /analyticscode
WORKDIR /analyticscode
ADD requirements.txt /analyticscode/
RUN pip install -r requirements.txt

#CMD python manage.py collectstatic --no-input
#CMD python manage.py runserver 0.0.0.0:8030

CMD sleep infinity