# Star Wars Favourites App (SWFA)
## Introduction

**SWFA** is a simple app for fetching Star Wars planet and movie information. It provides API for following functionality:
- List all planets and movies.
- Add a movie and planet as a favorite.
- Add custom name/title to a movie or planet.
- Search for a planet/movie based on name/title.
- List all movies of a planet.
- List favourite movies/planets

### Future:
- Adds User and User Authentication
- Adds user based favourites and custom names


## APIs
### Planet

- `GET /api/planets/:id/` 
  - get a specific planet resource

- `POST /api/planets/:id/favourite/`
  - mark a specific planet as favourite or remove from favourite.
  - requestBody:
      - required: `false`

- `POST /api/planets/:id/custom-name/`
  - Adds custom name to planet
  - requestBody:
     ```json
    {
        "custom_name": <string>
    }
     ```

- `GET /api/planets/`
  - Returns all the planets
  - Query Strings
    - `page`: `<page_number: integer>`
       - ex: `/api/planets/?page=2` 
    - `search`: `<search_query: string>`
       - Filters the set of resources returned.
       - ex: `/api/planets?search=Tat`

- `GET /api/planets/favourites/`
  - Returns all the favourite planets

- `GET /api/planets/:id/movies/`
  - List all movies of a planet.

### Movies

- `GET /api/movies/:id/` 
  - get a specific movie resource

- `POST /api/movies/:id/favourite/`
  - mark a specific movie as favourite or remove from favourite.
  - requestBody:
      - required: `false`

- `POST /api/movies/:id/custom-name/`
  - Adds custom name to movie
  - requestBody:
     ```json
    {
        "custom_name": <string>
    }
     ```

- `GET /api/movies/`
  - Returns all the movies
  - Query Strings
    - `page`: `<page_number: integer>`
       - ex: `/api/movies/?page=2` 
    - `search`: `<search_query: string>`
       - Filters the set of resources returned.
       - ex: `/api/movies?search=Tat`

- `GET /api/movies/favourites/`
  - Returns all the favourite movies

## Setup

### Clone the repo and move to the directory
```bash
git clone https://github.com/preethihena/StarWars-Favourites.git
cd StarWars-Favourites/
```

### Create a virtual environment and activate it
```bash
python3 -m venv env
source env/bin/activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Setting up database
```bash
python manage.py makemigrations
python manage.py migrate
```

In case migrations are not found run:
```bash
python manage.py makemigrations favourites
```

### Running API
```bash
python manage.py runserver
```

### Running Tests
```bash
python manage.py test
```