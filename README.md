run rabbitmq container:
# docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 rabbitmq

run postgres container:
# docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=qwerty -d postgres:15.1

connect to postgres container from localhost:
# psql -h localhost -p 5432 -U postgres

exec into postgres container:
# docker exec -it some-postgres bash
# psql -U postgres
# CREATE DATABASE nutrition;
# \c nutrition;
# CREATE TABLE IF NOT EXISTS files ( id SERIAL PRIMARY KEY, filename varchar(45) NOT NULL, date varchar(20));
# \dt (list tables inside public schemas)

check if the data was successfully inserted into db table:
# psql -h localhost -p 5432 -U postgres
# \c nutrition;
# SELECT * FROM files;

create and run Python container:
# docker build -t receiver-app .
# docker run -it --rm --name receiver-app-container --link some-rabbit:rabbit-link --link some-postgres:postgres-link receiver_app