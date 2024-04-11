# Use the official MongoDB image
FROM mongo:4.4-focal

# Expose MongoDB port
EXPOSE 27017

# Define environment variable for MongoDB database
ENV MONGO_INITDB_DATABASE=quiz_app

# Copy the MongoDB data files into the container
COPY ./quiz_app /docker-entrypoint-initdb.d/

# Set the permissions to allow MongoDB to access the files
RUN chown -R mongodb:mongodb /docker-entrypoint-initdb.d/

# This script will be executed during container startup
COPY ./entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]
CMD ["mongod", "--port", "27018"]  # Change the default MongoDB port to 27018

