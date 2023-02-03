#write how to stop all the containers, delete them and their images and build new

# Rabbitmq:
docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 rabbitmq

# Postgres:
docker build -t my-postgres --no-cache -f Dockerfile_postgres .
docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=qwerty -d my-postgres

# Python for file processing:
docker build -t file_processing -f Dockerfile_fp .
# docker run -it --rm --name file_processing --link some-rabbit:rabbit-link --link some-postgres:postgres-link file_processing

# Python for loading product page:
docker build -t page_loader -f Dockerfile_pl .
# docker run -it --rm --name page_loader --link some-rabbit:rabbit-link --link some-postgres:postgres-link page_loader

run Django container for UI:
# docker build -t user_interface -f Dockerfile_ui .
# docker run -it --rm --name user_interface --link some-rabbit:rabbit-link --link some-postgres:postgres-link user_interface 
docker run -it --rm --name user_interface --link some-postgres:postgres-link user_interface 
