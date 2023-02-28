Project Nutrition is written to track the nutrition value of the products the family consumes withing a week. It provides a user interface where a user can upload a PDF receipt from a grocery store and see the avarage daily nutrition value of the purchased products.

Following technologies were used in this project: Python 3.7, Django 3.2.16 (libraries - psycopg2, pika), PostgreSQL, RabbitMQ, jQuery, Bootstrap, Docker, Git.

Here is a schema of the project:

![alt text](/drawio.png?raw=true)

To run the project you need a `docker-compose` installed on your machine.
Open the terminal and go to the project's root folder. Then run a command:
```
$ docker-compose up
```
Now the project should be available from your browser by a link: http://127.25.0.5:8000/
