# Food Repo User API
API to manage users of the [Food Repo](https://github.com/arturomorarioja/web_e24_ux_food_repo) application.

## Endpoints

POST parameters are sent as form-data.

|Method|Endpoint|POST params|
|------|--------|-----------|
|POST|/users|email, first_name, last_name, password|
|POST|/validation|email, password|
|GET|/users/<user_id>/favourites||
|POST|/users/<user_id>/favourites|recipe_id|
|DELETE|/users/<user_id>/favourites/recipe_id||

## Installation
Python 3.4 or higher required.

1. Create a virtual environment:
```
python -m venv venv
```

2. Activate the virtual environment.
- Windows cmd: `.\venv\Scripts\activate`
- Windows Powershell: `.\venv\Scripts\Activate`
- Linux and Mac: `source venv/bin/activate`

3. Install dependencies:
```
pip install -r requirements.txt
```

4. If this is the first time the API is run, create the database:
```
python -m flask --app food_repo_users init-db
```

## Running the API
Within (venv), run:
```
python -m flask --app food_repo_users run --port 8001 --debug
```
The endpoints will be available at `http://localhost:8001`.

## Tools
SQLite / Flask / Python

## Author
Arturo Mora-Rioja