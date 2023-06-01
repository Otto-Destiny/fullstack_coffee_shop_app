# Coffee Shop Full Stack Application

Welcome to the Coffee Shop Full Stack Application! This application serves as a backend API for managing drinks in a coffee shop. It provides endpoints for creating, retrieving, updating, and deleting drinks, as well as authentication and authorization functionality.

The backend of the Coffee Shop application is built with Flask, a lightweight and flexible web framework for Python. It uses SQLAlchemy as the Object-Relational Mapping (ORM) tool for working with the database(sqlite3). The authentication and authorization are implemented using JSON Web Tokens (JWT) and role-based access control (RBAC) with the help of Auth0.

This README file provides an overview of the Coffee Shop API, including the setup instructions, available endpoints, authentication and authorization details, testing instructions, and deployment guidelines. It also includes information about the frontend application built with Ionic Framework, which interacts with the backend API.

In addition, the app also has these capabilities:
1. Display graphics representing the ratios of ingredients in each drink.
2. Allow public users to view drink names and graphics.
3. Allow the shop baristas to see the recipe information.
4. Allow the shop managers to create new drinks and edit existing drinks.

## Coffee Shop App Backend
This is the backend code for the Coffee Shop App. It provides an API for managing drinks in the coffee shop.

### Getting Started
To get started with the Coffee Shop App backend, follow these steps:

Clone the repository: `git clone https://github.com/your-repo-url.git`
Navigate to the backend directory: `cd Coffee_Shop_App/backend`
Install the dependencies: `pip install -r requirements.txt`
Set up the database: Uncomment the line `db_drop_and_create_all()` in the code to initialize the database on the first run. Note that this will drop all existing records and start the database from scratch. Make sure to comment this line after the initial run.
Start the server: `flask run`

#### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### API Endpoints
The Coffee Shop App backend provides the following API endpoints:

#### Get Drinks
Endpoint: `/drinks`
Method: GET
Description: Retrieves a list of drinks in the coffee shop.
Permissions: Public
Request Parameters: None
Response:
- Status Code: 200 OK
- Body: JSON object with the following structure:
``` {
  "success": true,
  "drinks": [
    {
      "id": 1,
      "title": "Americano"
    },
    {
      "id": 2,
      "title": "Latte"
    },
    ...
  ]
}
```
- Error Handling: Returns appropriate status code and error message in case of failure.

#### Create Drink
Endpoint: `/drinks`
Method: POST
Description: Creates a new drink in the coffee shop.
Permissions: Requires authentication with post:drinks scope
Request Body:
JSON object with the following structure:
```
{
  "title": "Drink Title",
  "recipe": [
    {
      "name": "Ingredient 1",
      "color": "Ingredient Color",
      "parts": 1
    },
    ...
  ]
}
```
Response:
Status Code: 201 Created
Body: JSON object with the following structure:
```
{
  "success": true,
  "drinks": [
    {
      "id": 1,
      "title": "Drink Title",
      "recipe": [
        {
          "name": "Ingredient 1",
          "color": "Ingredient Color",
          "parts": 1
        },
        ...
      ]
    }
  ]
}
```
Error Handling: Returns appropriate status code and error message in case of failure.

#### Get Drink Details
Endpoint: `/drinks-detail`
Method: GET
Description: Retrieves the details of all drinks in the coffee shop.
Permissions: Requires authentication with get:drinks-detail scope
Request Parameters: None
Response:
Status Code: 200 OK
Body: JSON object with the following structure:
```
{
  "success": true,
  "drinks": [
    {
      "id": 1,
      "title": "Drink Title",
      "recipe": [
        {
          "name": "Ingredient 1",
          "color": "Ingredient Color",
          "parts": 1
        },
        ...
      ]
    },
    ...
  ]
}
```
Error Handling: Returns appropriate status code and error message in case of failure.

#### Update Drink
Endpoint: `/drinks/<id>`
Method: PATCH
Description: Updates an existing drink in the coffee shop.
Permissions: Requires authentication with `patch:drinks` scope
Request Parameters:
`<id>`: The ID of the drink to be updated.
Request Body:
JSON object with the following structure:
```
{
  "title": "Updated Drink Title",
  "recipe": [
    {
      "name": "Updated Ingredient 1",
      "color": "Updated Ingredient Color",
      "parts": 2
    },
    ...
  ]
}
```
Response:
Status Code: 200 OK
Body: JSON object with the following structure:
```
{
  "success": true,
  "drinks": [
    {
      "id": 1,
      "title": "Updated Drink Title",
      "recipe": [
        {
          "name": "Updated Ingredient 1",
          "color": "Updated Ingredient Color",
          "parts": 2
        },
        ...
      ]
    }
  ]
}
```
Error Handling: Returns appropriate status code and error message in case of failure.

#### Delete Drink
Endpoint: `/drinks/<id>`
Method: DELETE
Description: Deletes an existing drink from the coffee shop.
Permissions: Requires authentication with `delete:drinks` scope
Request Parameters:
`<id>`: The ID of the drink to be deleted.
Response:
Status Code: 200 OK
Body: JSON object with the following structure:
```
{
  "success": true,
  "delete": 1
}
```
Error Handling: Returns appropriate status code and error message in case of failure.



Please note that these endpoints require authentication with specific scopes to access or modify the data.

### Error Handling
The Coffee Shop App backend handles errors in the following way:

400 Bad Request: Missing required fields or invalid request.
401 Unauthorized: Authentication failure or invalid token.
403 Forbidden: The authenticated user does not have permission to access the resource.
404 Not Found: The requested resource is not found.
500 Internal Server Error: Unexpected server error occurred.

### Authentication and Permissions

The Coffee Shop API uses authentication and role-based access control (RBAC) to secure the endpoints. The authentication is implemented using JWT (JSON Web Tokens) and the permissions are enforced using the requires_auth decorator.

To authenticate and authorize requests, the API uses Auth0, a flexible and scalable authentication and authorization platform. Auth0 provides a simple way to add authentication and authorization to your applications, and it supports various authentication methods such as username/password, social logins, and more.

The Coffee Shop API includes the following roles and permissions:

Barista Role
`get:drinks-detail`: Can view drink details.
`get:drinks`: Can view drinks.
Manager Role
`post:drinks`: Can create new drinks.
`patch:drinks`: Can update existing drinks.
`delete:drinks`: Can delete drinks.
Inherits all permissions from the Barista role.
To access the protected endpoints, you need to include a valid JWT token in the `Authorization` header of your requests. The token should be prefixed with the word `Bearer` followed by a space.

### Testing
The Coffee Shop API includes a comprehensive test suite to ensure the correctness of the implemented functionality. The tests cover both positive and negative scenarios, including authentication, authorization, and endpoint functionality.

To run the tests, follow these steps:

Set up a test database.
Update the database URI to point to the test database.
Open a terminal or command prompt.
Navigate to the project root directory.
Run the following command to install the required testing dependencies:
Copy code
```
pip install -r requirements.txt
```
Run the tests using the following command:
Copy code
```
python test_app.py
```
This command will execute the test suite and display the results on the terminal.
The test suite includes tests for each endpoint, testing both successful and error cases. It covers authentication, authorization, and the expected behavior of each endpoint.

Please note that running the tests will modify the test database. It's recommended to use a separate database for testing purposes to ensure the integrity of your development or production data.

## Coffee Shop Frontend
The Coffee Shop Frontend is a user interface built with Ionic Framework, a popular open-source framework for developing cross-platform mobile and web applications using web technologies such as HTML, CSS, and JavaScript.

The frontend of the Coffee Shop application provides a user-friendly interface for customers and staff to interact with the Coffee Shop API. It allows users to view available drinks, add new drinks to the menu, update existing drinks, and delete drinks. The frontend also handles user authentication and authorization to ensure secure access to the API endpoints.

### Features
The Coffee Shop Frontend includes the following features:

Drink Listing: Users can view a list of available drinks along with their details, such as title and ingredients.
Drink Creation: Staff members with the appropriate permissions can add new drinks to the menu by providing the title and recipe.
Drink Editing: Staff members can update the details of existing drinks, including the title and recipe.
Drink Deletion: Staff members can remove drinks from the menu.
User Authentication: The frontend provides a login functionality for users to authenticate themselves using their credentials.
### Installation
To install and run the Coffee Shop Frontend, follow these steps:

Ensure that you have Node.js and npm (Node Package Manager) installed on your machine.
Clone the repository for the Coffee Shop Frontend from the provided source.
Open a terminal or command prompt and navigate to the project directory.
Run the following command to install the required dependencies:
Copy code
```
npm install
```
After the dependencies are installed, run the following command to start the frontend application:
Copy code
```
ionic serve
```
The frontend application will be served locally at `http://localhost:8100`. Open a web browser and access this URL to view the Coffee Shop application.
Please note that the frontend application may require additional configuration to connect with the backend API. Make sure to update the API endpoint and authentication details in the frontend code to ensure proper communication with the backend.

### Usage
The Coffee Shop Frontend provides an intuitive user interface for interacting with the Coffee Shop API. Users can navigate through the available pages to perform various actions, such as viewing drinks, adding new drinks, updating existing drinks, and deleting drinks. The frontend handles authentication and authorization automatically, ensuring that users have the necessary permissions to access certain features.

## Deployment
To deploy the Coffee Shop API to a production environment, follow these steps:

Set up a production database.
Update the database URI to point to the production database.
Configure the necessary environment variables, such as the Auth0 credentials and database URI.
Set up a production-ready web server, such as Nginx or Apache, to handle incoming requests.
Deploy the Flask application to the web server, following the recommended deployment practices for your chosen web server.
Configure SSL/TLS certificates to enable secure communication with the API.
Start the web server and ensure that the API is accessible over HTTPS.
It's important to secure your production environment by properly configuring authentication, authorization, and access control mechanisms. You should also monitor the application for performance, security, and error logging to ensure smooth operation.

## Author
Yours truly, Destiny Otto