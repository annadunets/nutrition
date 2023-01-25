Run bash script to build all needed docker containers:
# ./scripts/script.sh

run Python container for file processing:
# docker run -it --rm --name file_processing --link some-rabbit:rabbit-link --link some-postgres:postgres-link file_processing

run Python container for loading product page:
# docker run -it --rm --name page_loader --link some-rabbit:rabbit-link --link some-postgres:postgres-link page_loader