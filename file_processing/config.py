from os.path import dirname, abspath

# declare constants

# database:
DATABASE="nutrition"
DB_HOST="some-postgres"
DB_USER="postgres"
DB_PASSWORD="qwerty"
DB_PORT="5432"

# message queue:
MQ_HOSTNAME = "some-rabbit"

# filepath
MAINDIR = str(dirname(dirname(abspath(__file__))))
