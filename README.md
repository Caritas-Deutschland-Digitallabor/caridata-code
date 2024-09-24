# CariData

built with <br>
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Setup

### Development Environment (using VSCode)

This project is set up in a Devcontainer, which means all developement is done in a Docker container. This container runs on Ubuntu Jammy, contains a vscode instance with predefined extensions, settings and tasks. It also contains a Python3.11 distribution (with pyenv and poetry), a Nodejs LTS (v20) distribution.

### How to start the Dev Container (using VSCode)

1. Have this repository cloned to your machine and open it in VSCode
2. Add or update the .env-file to the [backend/src/](backend/src/) folder. You can find a up-to-date .env-file in Bitwarden under the CariData collection.
3. Install the following dependencies
   - [Dev Containers extension](vscode:extension/ms-vscode-remote.remote-containers) for VSCode
   - [Docker Desktop](https://docs.docker.com/desktop/install/mac-install/)
4. If you are prompted by VSCode, hit "Reopen in Container". If not, open the command palette (`F1` or `cmd + shift + p` on Mac) and look for "Dev Containers: Reopen in Container"
   - If you are prompted to decide on a container, hit "fullstack-container"
5. Now wait a bit while Docker pulls images, builds new images, builds the container(s), opens VSCode in a container and installs lots of stuff. This might take a few minutes. But don't worry, the next time you open this dev environment it will only take a few seconds.
6. At this point you should be able to see the contents of this repository opened in a new working directory called "workspace". Everything in "workspace" is mounted to your local machine, so changes made inside the devcontainer will also be reflected outside the container on your machine. You can also use git from inside this container. Additionally, VSCode will have opened 2 terminals running a FastAPI instance [localhost:8000](http://localhost:8000/docs#) and the frontend [localhost:3000](http://localhost:3000) on hot reload.
   - If there is a "command uvicorn not found" error in the FastAPI terminal, open the command palette and do "Tasks: Run Task" -> "FastAPI: Run" -> "Continue without scanning the task input"
   - If the problem persists do `make api-start` in a terminal from root
7. Start developing

### How to troubleshoot

#### During Setup

If the devcontainer had an error while setting up you should try out the following individual approaches (in escalating order)

- command palette: "Dev Containers: Rebuild and Reopen in Container" (will take a bit)
- command palette: "Dev Containers: Rebuild Without Cache and Reopen in Container" (will take longer)

If you are still experiencing issues look into the dev container log using: command palette: "Dev Containers: Show Container Log" and if you are confident enough try modifying the dev container configuration accordingly.

You can find additional information to understand this setup under [./docs/tools](./docs/tools)

#### Gitlab

If you are not able to pull from or push to Gitlab your ssh-agent configuration may be at fault.

- open a terminal and run the following with the private key being the counterpart to your public key on Gitlab <br>
  `ssh-add --apple-use-keychain ~/.ssh/[your-private-key]`
- add the following to your `~/.ssh/config` to enforce usage of the keychain <br>
  ```bash
  Host *
    UseKeychain yes
    AddKeysToAgent yes
    IdentityFile ~/.ssh/[your-private-key]
  ```

#### Help, everything worked before and now after I pulled the latest version of this branch my Devcontainer does not work anymore!

##### alembic and database issues

If your Container suddenly starts to close itself after you pulled the latest branches there might be an issue with the commands executed by docker compose.
Have a look into the logs of the docker container (either via Docker Desktop or VS Code).

One common issue could be the difference between the migration of your local postgres volume and the assumed migration state. See the [migration files](backend/src/database/migrations/versions). This difference leads to an error in an alembic upgrade command which shuts the container down.

To fix this issue backup (optional) and delete your projects local postgres volume and the relevant postgres container. Afterwards run "Dev Containers: Rebuild Without Cache and Reopen in Container" via the command palette.

##### .env not up to date

If your Container suddenly starts to close itself after you pulled the latest branches there might be an issue your .env file.
Have a look into the logs of the docker container (either via Docker Desktop or VS Code).

To fix this issue, update your local .env with the one found in this projects Bitwarden collection.

#### Aggregation Language (aggregation_schemas.json)

Possible Filter conditions:
"=": "eq"
"!=": "ne"
">": "gt"
"<": "lt"
">=": "gte"
"<=": "lte"
"IS" && value == NULL: "is_null"
"IS NOT" && value == NULL: "is_not_null"

The difference between "IS" and "=" is that "IS" is used to compare with NULL values (so undefined, empty string etc) while "=" is used to compare with actual values.
The same applies to "IS NOT" and "!=". "IS" and "IN NOT" will only work with NULL values and will not work with actual values. This is equivalent to the way SQL handles the comparisons of values.
