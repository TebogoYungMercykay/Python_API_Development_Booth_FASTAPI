# FastAPI: Main Source Directory

### Quick Setup for Running the Python API

- ###### Creating the Python Virtual Environment:
    ```bash
    - sudo apt-get update
    - sudo apt-get install python3-venv
    - python3 -m venv venv

    - pip install virtualenv
    - virtualenv -p python3 <env_name>
    - source <env_name>/bin/activate
    - deactivate
    ```

- ###### Activating the Python Virtual Environment:
    ```bash
    - source venv/bin/activate
    ```

- ###### Deactivating the Python Virtual Environment:
    ```bash
    - deactivate
    ```

- ###### FastAPI:
    ```bash
    - pip install fastapi[all]
    - python.exe -  pip install autopen8
    # checking the installed packages
    - pip freeze # paste them in the requirements.txt file
    - Running the API:
        - univorn app/main:app
        - univorn app/main:app --reload (for automatic updates)
    ```


### Some of the API Routes and Functionality

- ###### Post route

    ```bash
    This route is reponsible for CRUD operations for posts/feed
    ```

- ###### Users route

    ```bash
    This route is about CRUD operations for users
    ```

- ###### Auth route

    ```bash
    This route is about login/logout system
    ```

- ###### Vote route

    ```bash
    This route is about likes or vote system and this route contain code for upvote or back vote there is not logic about down vote
    ```

- ###### Diseases route
    ```bash
    This route is Responsible for the CRUD operations on the diseases tables and the information
    ```

- ###### Chat
    ```bash
    This route is about the Chat/Video functionality between the Doctor and the Patient
    ```

- ###### Consultation route
    ```bash
    This route is responsible for the starting and ending a Consultation between the Doctor and the Patient
    ```


### Testing the API on Google
- ###### Go to https://google.com
- ###### Go to Developer Tools
- ###### Go to The Console Window
- ###### Type:
    ```python
    fetch('http://localhost:8000/').then(result => result.json().then(console.log))
    ```


### How To Run Locally
- ###### 1. First clone this repo by using following command
    ```
    cd path/to/api
    ```

- ###### 2. Then install fastapp using all flag like 
    ```
    pip install fastapi[all]
    ```

- ###### 3. The go this repo folder in your local computer run follwoing command
    ```
    uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
    ```

- ###### 4. Then you can use following link to use the  API
    ```
    http://127.0.0.1:8000/docs 
    ```

### To Run This API You Need a Database in Postgres (Just a Recommendation)

- ###### 1. Create a database in postgres then create a file name .env and write the following things in you file 
    ```
    DATABASE_HOSTNAME='DATABASE_HOSTNAME'
    DATABASE_PORT='DATABASE_PORT'
    DATABASE_PASSWORD='DATABASE_PASSWORD'
    DATABASE_NAME='DATABASE_NAME'
    DATABASE_USERNAME='DATABASE_USERNAME'
    SECRET_KEY='SECRET_KEY'
    ALGORITHM='ALGORITHM'
    ACCESS_TOKEN_EXPIRE_MINUTES='ACCESS_TOKEN_EXPIRE_MINUTES'
    ```
- ###### 2. Note: SECRET_KEY in this example is just a psudo key. You need to get a key for youself and you can get the SECRET_KEY from fastapi documantion

- ###### 3. Installing Requirements:
    ```bash
    - Using a Script to Skip Failed ones:
        - Making the File Executable:
            chmod +x requirements_script.sh
        - Running the Script:
            ./requirements_script.sh
    - Default way to install:
        pip install -r requirements.txt
    ```
---

### Deploying the Application on Heroku
- ###### 1. Command line arguments
    ```bash
    sudo snap install heroku --classic
    heroku --version
    heroku login
    heroku create healthconnect-python-fastapi
    # Pushing code to Heroku: git push heroku master
        - git add --all
        - git commmit -m "message"
        - git push origin master
        - git push heroku master
    ```

---
---

<p align="center">The End, Thank You!</p>

---
