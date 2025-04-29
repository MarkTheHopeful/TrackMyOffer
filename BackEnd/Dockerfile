FROM gradle:8.5-jdk17 AS build

WORKDIR /app
COPY . /app/
RUN gradle build --no-daemon

FROM eclipse-temurin:17-jre

WORKDIR /app
COPY --from=build /app/build/libs/*.jar /app/server.jar

# Default environment variables
ENV PORT=8080
ENV HOST=0.0.0.0

# Expose the port
EXPOSE $PORT

# Run the application
ENTRYPOINT ["java", "-jar", "/app/server.jar"]
