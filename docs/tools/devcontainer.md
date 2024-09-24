# DevContainers
DevContainers, or Development Containers, in Visual Studio Code are a part of the Remote - Containers extension. They provide a fully configured and isolated development environment that can be shared across your team.

The main idea is to define your development environment as code inside a Docker container. This includes the operating system, system libraries, command-line utilities, programming languages, or anything else your application needs to run.

This configuration is stored in a file called [devcontainer.json](../../.devcontainer/fullstack-container/devcontainer.json) and optionally a Dockerfile and/or a [docker-compose.yaml](../../.devcontainer/docker-compose.yml) in a .devcontainer directory in your project. When you open your project in VS Code, it will automatically build (if necessary) and start the container based on this configuration.

This approach has several benefits:

- __Consistency__: Everyone on your team will have the exact same development environment, reducing the "it works on my machine" problem.
- __Isolation__: Dependencies of your project are isolated from your local machine, keeping it clean.
- __Portability__: You can work on your project from any machine that has Docker and VS Code installed.
- __Simplified Onboarding__: New developers can quickly set up the development environment by simply opening the project in VS Code.
- __Versioning__: The development environment configuration can be versioned along with your source code, allowing you to go back in time if needed.

To start using DevContainers, you only need to have Docker installed on your machine and the Dev Containers extension installed in VS Code.

## The Dockerfile

Here's a breakdown of what's happening in the [Dockerfile](../../.devcontainer/fullstack-container/Dockerfile):

__Lines 21-42__: These lines are installing a number of development libraries needed for various Python packages and other tools. pre-commit is also installed, which is a framework for managing and maintaining multi-language pre-commit hooks.

__Lines 45-46__: These lines are installing Node.js version 20.x and npm. The exact version of Node.js that gets installed depends on the latest version in the 20.x series available from the nodesource repository at the time the Docker image is built.

__Lines 49-61__: These lines are configuring the global npm install location. It first checks if a group named "npm" exists, if not, it creates one. Then it adds the root user to the npm group. It sets the umask to 0002 to ensure that any new files and directories are writable by the group. It then creates the global npm directory and sets its ownership and permissions. It also sets the global npm prefix to this directory for both the root user and the user "vscode". Finally, it installs the eslint package globally and cleans the npm cache.

__Lines 64-75__: These lines switch the user to "vscode" and install Python using pyenv. Pyenv is a simple, powerful and cross-platform tool for managing multiple Python versions. It's installing the Python version specified by the PYTHON_VERSION environment variable.

This Dockerfile is designed to create a consistent, reproducible development environment that has all the necessary dependencies for a Node.js and Python project.

## The Docker-Compose.yml

This [docker-compose.yml](../../.devcontainer/docker-compose.yml) file defines two services: fullstack and db. Here's a breakdown of what each service does:

__fullstack Service (Lines 4-20)__: This service builds a Docker image using the Dockerfile located at ./fullstack-container/Dockerfile. The build context is set to the current directory (.). The service mounts the parent directory (..) to /workspace inside the container. It depends on the db service, meaning it will start only after the db service has started. The command section runs a series of commands inside the container, including setting a git configuration, installing Python dependencies with Poetry, installing pre-commit hooks, running database migrations with Alembic, and then putting the container to sleep indefinitely, to keep it running. This last step ensures that you can enter the container and start developing.

__db Service (Lines 22-32)__: This service uses the postgres:latest Docker image and restarts unless manually stopped. It mounts a named volume postgres-data to /var/lib/postgresql/data inside the container, which is where PostgreSQL stores its data. It sets environment variables for the PostgreSQL password, user, and database name.

__volumes (Lines 34-35)__: This section defines a named volume postgres-data. This volume is used by the db service to persist PostgreSQL data across container restarts.

In summary, this Docker Compose file sets up a development environment with two services: a full-stack application and a PostgreSQL database. The full-stack application service installs its dependencies and runs database migrations when it starts, and the PostgreSQL service is configured with a persistent volume for data storage.
