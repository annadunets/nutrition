Run bash script to build all needed docker containers:
# ./scripts/script.sh

run Python container for file processing:
docker build -t file_processing --no-cache -f Dockerfile_fp .
# docker run -it --rm -d --name file_processing --link some-rabbit:rabbit-link --link some-postgres:postgres-link file_processing

run Python container for loading product page:
docker build -t page_loader --no-cache -f Dockerfile_pl .
# docker run -it --rm --name page_loader --link some-rabbit:rabbit-link --link some-postgres:postgres-link page_loader