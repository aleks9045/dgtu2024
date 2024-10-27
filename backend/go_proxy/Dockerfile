# Start with the scratch image
FROM scratch

# Set a working directory
# RUN mkdir /app
WORKDIR /app

# Copy the entire project
COPY ./exe ./bin

# Expose the port
EXPOSE "8083:8083"

# Specify the command to run
CMD ["./bin/app"]
