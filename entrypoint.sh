#!/bin/bash
set -e
# Run mongod in the background
mongod --fork --logpath /var/log/mongodb.log --bind_ip_all
# Import the data into the specified database
mongorestore --db quiz_app --drop /docker-entrypoint-initdb.d/quiz_app
# Revert to the original CMD
exec "$@"

