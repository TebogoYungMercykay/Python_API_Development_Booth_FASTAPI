# FastAPI: Python_API_Development_Booth

### Quick Setup for the Python API

- ###### Creating the Python Virtual Environment:
    ```markdown
    - sudo apt-get update
    - sudo apt-get install python3-venv
    - python3 -m venv venv

    - pip install virtualenv
    - virtualenv -p python3 <env_name>
    - source <env_name>/bin/activate
    - deactivate
    ```

- ###### Activating the Python Virtual Environment:
    ```markdown
    - source venv/bin/activate
    ```

- ###### Deactivating the Python Virtual Environment:
    ```markdown
    - deactivate
    ```

- ###### FastAPI:
    ```markdown
    - pip install fastapi[all]
    - pip freeze
    - python.exe -  pip install autopen8
    - Running the API:
        - univorn app/main:app
        - univorn app/main:app --reload (for automatic updates)
    ```


### This API  has 4 routes

- ###### 1. Post route

    ```markdown
    This route is reponsible for creating post, deleting post, updating post and Checkinh post
    ```

- ###### 2. Users route

    ```markdown
    This route is about creating users and searching user by id
    ```

- ###### 3. Auth route

    ```markdown
    This route is about login system
    ```

- ###### 4. Vote route

    ```markdown
    This route is about likes or vote system and this route contain code for upvote or back vote there is not logic about down vote
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
    uvicorn main:app --reload
    ```

- ###### 4. Then you can use following link to use the  API
    ```
    http://127.0.0.1:8000/docs 
    ```

### To Run This API You Need a Database in Postgres (Just a Recommendation)

- ###### 1. Create a database in postgres then create a file name .env and write the following things in you file 
    ```
    DATABASE_HOSTNAME = localhost
    DATABASE_PORT = 5432
    DATABASE_PASSWORD = passward_that_you_set
    DATABASE_NAME = name_of_database
    DATABASE_USERNAME = User_name
    SECRET_KEY = 09d25e094faa2556c818166b7a99f6f0f4c3b88e8d3e7 
    ALGORITHM = HS256
    ACCESS_TOKEN_EXPIRE_MINUTES = 60(base)
    ```
- ###### 2. Note: SECRET_KEY in this example is just a psudo key. You need to get a key for youself and you can get the SECRET_KEY from fastapi documantion

- ###### 3. Installing Requirements:
    ```markdown
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

<p align="center">The End, Thank You!</p>

---
