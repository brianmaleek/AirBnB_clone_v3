# Flask API project. 

## The project structure map is as follows:

```table
api/
├── __init__.py
├── v1/
│   ├── __init__.py
│   ├── app.py
│   ├── views/
│   │   ├── __init__.py
│   │   └── index.py
```

## The project is organized as follows:

- `api/`: Root folder for the API
  - `__init__.py`: An empty file to initialize the API package.
  - v1/: Version 1 of the API
    - `__init__.py`: Initializes version 1 of the API.
    - `app.py`: Defines the Flask app, imports storage, and registers blueprints.
  - `views/`: Contains the views of the API.
    `__init__.p`y: Initializes the API views.
    - `index.py`: Contains the routes for the API, including a status route.

The app.py file contains the following code:

```Python
import storage from models
import app_views from api.v1.views

app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def close_db(e):
    storage.close()

if __name__ == '__main__':
    app.run(host=os.environ.get('HBNB_API_HOST', '0.0.0.0'),
              port=os.environ.get('HBNB_API_PORT', 5000),
              threaded=True)
```

The `app_views` variable is an instance of the `Blueprint` class, which is used to organize and register groups of related routes. The `url_prefix` argument to the `Blueprint` constructor specifies the prefix that will be prepended to all of the routes in the blueprint. In this case, the prefix is `/api/v1`.

The `views/__init__.py` file contains the following code:

```Python
from flask import Blueprint

app_views = Blueprint('api_v1', __name__, url_prefix='/api/v1')

from . import index
Use code with caution. Learn more
The index.py file contains the following code:

Python
from api.v1.views import app_views

@app_views.route('/status')
def status():
    return jsonify({'status': 'OK'})
```

## Usage

To run the project, follow these steps:

Navigate to the project directory if you are not already there.

Ensure that you have activated your virtual environment (if created).

Run the Flask server.

To start the Flask server, run the following command:

```python
python api/v1/app.py
``````

The server will be running on port `5000` by default. You can access the `API` endpoints at the following `URL`:

```python
http://localhost:5000/api/v1/
```

For example, to get the status of the API, you would send a `GET` request to the following URL:

```python
http://localhost:5000/api/v1/status
```

## Endpoints

The API provides the following endpoints:

- `GET /api/v1/status`: Returns a JSON object with the status information.

Example response:

The response would be a `JSON` object with the following contents:

```json
JSON
{
    "status": "OK"
}
```

## Testing

You can run the project's tests by executing the following command:

```python
python -m unittest discover tests
```
