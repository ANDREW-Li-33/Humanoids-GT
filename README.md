# Docker Setup

## Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- VSCode with the **Dev Containers** and **Docker** extensions installed

## Setup

1. Clone the repo and open it in VSCode
    ```
    git clone git@github.com:ANDREW-Li-33/Humanoids-GT.git
    ```

2. Build the Docker image
   ```bash
   docker compose build
   ```
   > You only need to re-run this when the Dockerfile changes.

3. Open the command palette (`Cmd+Shift+P` / `Ctrl+Shift+P`), select **Dev Containers: Reopen in Container**, then **From docker compose yaml file**

4. Open a new terminal in VSCode. You can run the commands below to verify that VSCode is inside the container
   ```bash
   lsb_release -a   # should show Ubuntu 20.04
   roscore          # open a second terminal and run rostopic list
   ```