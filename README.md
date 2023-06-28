# kartoza_assignment
This is a django web application that allow user to signup, signin, signout,
view profile, update profile and location on map.

## Prerequisites 
* python >= 3.8
* pip3

1. Clone the repository on you local machine with the command: 
    ```
    git clone https://github.com/shwetadev12/kartoza_assignment.git
    ```
2. Now move to repo with command:
    ```
    cd kartoza_assignment
    ```
3. Create a virtual environment. If you don't have virtualenv installed, you can download it with the command:
    ```
    pip install virtualenv
    
    ```
4. Create a virtual environment with the following command:
    ```
    virtualenv <virtual environment name>
    ```

5. Activate the virtual environment using the command:

    ```
    source <virtual environment name>/bin/activate
    ```
6. Install the app dependencies by running:
    ```
    pip install -r requirements.txt
    ```
7. Create a .env file in the backend directory using the command line:
    ```
    touch .env
    ```
8. Open the .env file and update it with the Postgres database credentials as follows:
    ```
    POSTGRES_DB=<postgres database name>
    POSTGRES_USER=<postgres user name>
    POSTGRES_PASSWORD=<postgres password>
    POSTGRES_HOST=<host name for postgres>
    POSTGRES_PORT=<postgres port>
    ```
9. For apply migrations run following command:
   ```
   python manage.py migrate
   ```
10. You can now run the backend server by executing the following command:
    ```
    python manage.py runserver
    ```
11. Now you can visit the application with command:
    ```
    http://127.0.0.1:8000/user/signup/
    ```
12. To Run test case:
   ```
   python manage.py test
   ```