run rabbitmq container:
# docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 rabbitmq

run postgres container:
# docker build -t my-postgres --no-cache -f Dockerfile_postgres .
# docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=qwerty -d my-postgres

create and run Python container:
# docker build -t receiver-app -f Dockerfile_fp .
# docker run -it --rm --name receiver-app-container --link some-rabbit:rabbit-link --link some-postgres:postgres-link receiver-app