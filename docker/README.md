# Docker - Containerization

Running the project locally in a Docker container. `Links`: [Docker Documentation](https://docs.docker.com/get-started/).

- ## `Dockerfile:`

    ```bash
    FROM python:3.9.7
    WORKDIR /usr/src/app
    COPY requirements.txt ./
    RUN pip install --no-cache-dir -r requirements.txt
    COPY . .
    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    ```

- ## `Docker Compose:`

    We use `docker-compose` to build and run multiple Docker container. This command uses a YAML file to configure the project's service in one go. Meaning, we create and start the service from our configuration file with a single command.

    - #### **Creating Images**:

        - We use the `docker-compose-prod.yaml` file to create an image for the service. Then, we run the following command to create images locally:

            ```yaml
            version: "3"
            services:
            api:
                image: tebogoyungmercykay/healthconnect:v1
                ports:
                - 80:8000
                environment:
                - DATABASE_HOSTNAME=${DATABASE_HOSTNAME}
                - DATABASE_PORT=${DATABASE_PORT}
                - DATABASE_PASSWORD=${DATABASE_PASSWORD}
                - DATABASE_NAME=${DATABASE_NAME}
                - DATABASE_USERNAME=${DATABASE_USERNAME}
                - SECRET_KEY=${SECRET_KEY}
                - ALGORITHM=${ALGORITHM}
                - ACCESS_TOKEN_EXPIRE_MINUTES=${ACCESS_TOKEN_EXPIRE_MINUTES}

                depends_on:
                - postgres

            postgres:
                image: postgres
                environment:
                - POSTGRES_PASSWORD=${DATABASE_PASSWORD}
                - POSTGRES_DB=${DATABASE_NAME}
                volumes:
                - postgres-db:/var/lib/postgresql/data

            volumes:
            postgres-db:
            ```

        - ###### Removing unused and dangling images:
            ```bash
            docker image prune--all
            ```
        - ###### Creating images locally:
            ```bash
            docker-compose -f docker-compose-dev.yaml build--parallel
            ```

    - #### **Running Containers**:

        - We run the containers using the images created in the step above. The `docker-compose.yaml` file will use the existing images and create containers. While creating containers, it defines the port mapping, and the container dependencies.

            ```yaml
            version: "3"
            services:
            postgres:
                image: postgres
                ports:
                    - 8080:8080
                restart: "always"  # no
            ```
        - **Starting the Project**:

            Once the `docker-compose-prod.yaml` file is ready we start the application using:

            ```bash
            docker-compose up
            ```

    > **NB**: YAML files are extremely indentation sensitive.


---

---

<p align="center">The End, Thank You!</p>

---