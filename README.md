# Kong Arthur Room Pricing Service

This application is a Flask-based REST API that handles CRUD operations for room pricing information. The data is stored in an SQLite database (`datarooms.db`), which is connected to a Docker volume to ensure persistent data.

## Functionality

The API offers the following features:

- Get room price by room type and season - Retrieves the dayly price for a specified room type in a given season.
- Update room price by room type and season - Updates the dayly price for a specified room type in a given season.

## Endpoints

### GET /rooms/<room_type>/<season>/
Returns the dayly price for the specified room type and season.

#### Response Code:

- `200 OK` - Successfully retrieved room price.
- `404 Not Found` - The specified room type or season could not be found.

**Example Request:**

```
GET /rooms/suite/low
```

**Example Response:**

```json
{
    "room_type": "suite",
    "season": "low",
    "dayly_price": 1500
}
```

### PUT /rooms/<room_type/season

Updates the dayly price for the specified room type and season.

#### Request Body:

The body must be in JSON format with the new price:

```json
{
    "dayly_price": 2000
}
```

#### Response Code:

- `200 OK` - Successfully updated the room price.
- `404 Not Found` - The specified room type or season could not be found.
- `400 Bad Request` - Invalid request body.

**Example Request:**

```
PUT /rooms/suite/low
```

**Example Request Body:**

```json
{
    "dayly_price": 2000
}
```

**Example Response:**

```json
{
    "message": "Dayly price updated"
}
```

## Installation

### Build and Run the Application

#### Build the Docker image:

```sh
docker build -t kong_arthur_room_price .
```

#### Run the Docker container with a volume binding:

```sh
docker run -it -p 5002:5002 -v miniprojekt:/app/data kong_arthur_room_price
```

This command builds and runs the Flask application, making it accessible on port `5002`.

