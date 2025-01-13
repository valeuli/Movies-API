README.md

# Movies API

Movies API is a project for managing movie information. It supports storage in **SQLite** or **MongoDB**, depending on the environment variable configuration. The project is built with **FastAPI**, **SQLAlchemy**, and **Pymongo**.

---

## **Prerequisites**

Make sure you have the following installed:

- **Python 3.12 or higher**
- **Pip** or **Pipenv** (for managing dependencies)
- **Docker** (optional, for MongoDB)
- **MongoDB** (if you choose MongoDB as the database)

---

## **Setup and Installation**

Follow these steps to install and run the project:

### **1. Clone the repository**
```bash
git clone https://github.com/valeuli/Movies-API.git
cd Movies-API
```
### **2. Set up a virtual environment**

Using Pipenv:
```bash
pipenv install
pipenv shell
```
Using venv:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
venv\Scripts\activate     # On Windows
pip install -r requirements.txt
```
### **3. Set environment variables**

Copy the `.env.example` file in the root directory and change the following content:

#### Repository type: sqlite or mongodb
```
REPOSITORY_TYPE="sqlite"
SQL_DATABASE_URL=<URL>
```
Note: You can use `sqlite:///../movies_project.db`

#### MongoDB configuration (only required if using MongoDB)
```
MONGO_DB_NAME="movies_db"

MONGO_URI="mongodb://localhost:27017"
```
Note: If you want to rune the application with the `docker compose` the value of the `MONGO_URI` must be `"mongodb://mongodb:27017"`
#### For the JWT Token Configuration
```SECRET_KEY="""
ALGORITHM=""
ACCESS_TOKEN_EXPIRE_MINUTES=30
```


### **4. Set up the database**
- SQLite: No additional setup is required. Tables will be created automatically when the project runs. 
- MongoDB: Ensure the MongoDB server is running. You can use Docker to spin up a MongoDB container:

```
docker run -d -p 27017:27017 --name movies-mongo mongo
```

#### 4.1 Populating the Database (SQLite only)
If you are using SQLite and want to pre-populate the database with public movies, you can run the following script:
```
python populate_database.py
```
This script inserts sample public movies into the SQLite database.
### **5. Run the application**

Start the FastAPI application using Uvicorn:

```
uvicorn main:app --reload
```

The API will be available at: http://localhost:8000

You can access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs 
- ReDoc: http://localhost:8000/redoc

### **6. Switching between SQLite and MongoDB**

To switch the database type, edit the `REPOSITORY_TYPE` variable in your .env file:
- For SQLite:

```
REPOSITORY_TYPE=sqlite
```

- For MongoDB:
```
REPOSITORY_TYPE=mongodb
```

And restart the server after making changes to the .env file.

## Running with Docker-compose
To run the application with `docker-compose` you can run the following command:
```
docker-compose up --build
```

## Running Tests

The project includes unit and integration tests to ensure functionality. To run the tests:
- Make sure you have pytest if not already installed:
```
pip install pytest
```

- Run the tests:
```
export IS_TEST=true; pytest
```
