# Use phusion/passenger-full as base image. To make your builds reproducible, make
# sure you lock down to a specific version, not to `latest`!
# See https://github.com/phusion/passenger-docker/blob/master/Changelog.md for
# a list of version numbers.
FROM phusion/passenger-full:1.0.9


# Set correct environment variables.
ENV HOME /root

# Use baseimage-docker's init process.
CMD ["/sbin/my_init"]


# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Enable Nginx
RUN rm -f /etc/service/nginx/down
RUN rm /etc/nginx/sites-enabled/default


ADD scripts/mb_api.conf /etc/nginx/sites-enabled/mb_api.conf


# Enable python
RUN apt-get update && apt-get install -y \
    python3-pip \
    libmysqlclient-dev \
    mysql-client


# Copy web application
RUN mkdir /home/app/mb_api
COPY --chown=app:app . /home/app/mb_api


RUN pip3 install Django==2.1.7 \
djangorestframework==3.9.1 \
djangorestframework-filters==1.0.0.dev0 \
django-cors-headers==2.4.0 \
django-rest-swagger==2.1.2 \
mysqlclient==1.4.2

RUN export PYTHONPATH=/usr/local/lib/python3.6/dist-packages/
