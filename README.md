# visualapproachanalytics

### Running the app locally

Create a virtual environment inside a root folder, then activate it.

# Create a virtual environment:

```
# Windows
python3 -m virtualenv .venv
# Or Linux
virtualenv .venv -p python3
```

# Activate virtual environment

```
# Windows
.venv\Scripts\activate
# Or Linux
source .venv/bin/activate
```

# Install the requirements with pip

```
pip install -r requirements.txt
```

# Build the docker container for db

```
docker-compose up -d db
```

# Create the configured database.

```
flask create-db
```

# Run app

```
flask run
```
