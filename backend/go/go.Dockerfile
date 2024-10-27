# Start with the scratch image
FROM scratch

# Set a working directory
# RUN mkdir /app
WORKDIR /app

# Copy the entire project
COPY ./exe ./bin
COPY ./config ./config

# Set environment variables
ENV HTTP_PORT=8084
ENV HTTP_REDIRECT_PORT=8053
ENV REDIRECT_URL=http://aleksey9045.fvds.ru:8053/v1/fit/callback

# Expose the port
EXPOSE 8084
EXPOSE 8053

# Specify the command to run
CMD ["./bin/app"]
