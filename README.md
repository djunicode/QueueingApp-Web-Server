# Queueing App Web Server
Django REST framework based web server for the Queueing App.

## Team Members
### Project Leader
Rudresh Panchal, Avais Pagarkar, Swapneel Mehta

### Mentors
Anant Joshi, Saumya Shah, Sarmishta Velury, Edward Gonsalves

### Developers
Sahil Jajodia


### Running it using Docker
First make sure you have Docker and docker-compose installed on your system.
Also make sure your local mysql server is **not** running.
Then navigate to this directory and type
```
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
docker-compose up
```
