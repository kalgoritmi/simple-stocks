## Simple Stocks Project

### Installation (Step by step)

Steps for local installation:
- Install `python` and `make`, I made use of `python 3.12`, assuming a debian based OS, adjust accorfing to your distribution:
    ```sh
    sudo apt install python3 make
    ```

- Create a virtual environment and install dependencies in it:
    ```sh
    make env
    ```

Steps for docker installation:
- Install `make`:
    ```sh
    sudo apt install make
    ```
- Install `docker` either follow instructions for the [official repo](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository) or install OS packaged version:
    ```sh
    sudo apt install docker.io 
    ```
- Run:
    ```sh
    make build-image
    ```
- Run:
    ```sh
    make run-image
    ```

Extra dev targets:
- Updating environment from requirements file:
    ```sh
    make env-update
    ```
- Freezing current environment and dumping package versions to the requirements file:
    ```
    make env-freeze
    ```
### Single step Installing & Running Main in Docker

Run main interactively:

```sh
make run-image
```
