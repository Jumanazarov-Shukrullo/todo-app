# TODO API Documentation

This document provides an overview of the API endpoints available in the Project Name project.

## Register User

### Endpoint: `api/register/`

- Method: `POST`
- Description: Register a new user.
- Parameters:
  - `username` (string): The username of the new user.
  - `password` (string): The password of the new user.
- Response:
  - Status Code: `201 Created`
  - Content: JSON object containing user details.

## Login User

### Endpoint: `api/login/`

- Method: `POST`
- Description: Log in an existing user.
- Parameters:
  - `username` (string): The username of the user.
  - `password` (string): The password of the user.
- Response:
  - Status Code: `200 OK`
  - Content: JSON object containing authentication token.

## List Todos

### Endpoint: `api/todo/all/`

- Method: `GET`
  - Description: 
  *Retrieve a list of all todos.
  - For the authenticated users show the authors of the todos
  - Able to filter by date
- Response:
  - Status Code: `200 OK`
  - Content: JSON array containing todo objects.

## Create Todo

### Endpoint: `api/todo/create/`

- Method: `POST`
- Description: 
  * Create a new todo.
  * Only authenticated users can create todos
- Parameters:
  - `title` (string): The title of the todo.
  - `description` (string): The description of the todo.
  - `author` (int): The id of the author
- Response:
  - Status Code: `201 Created`
  - Content: JSON object containing the created todo.

## Update  Todo

### Endpoint: `api/todo/<int:pk>/`

- Method: `PUT`
- Description:
  * Update todo by id.
  * Updates todos those created within 24 hours
- Parameters:
  - `title` (string, optional): The updated title of the todo.
  - `description` (string, optional): The updated description of the todo.
- Response:
  - Status Code:
    - `200 OK` for successful update.
    - `204 No Content` for successful deletion.
# Project Setup Instructions

To set up and run the Project Name project, follow these instructions:

1. **Clone the repository from GitHub:**
   ```sh
   git clone https://github.com/your-username/project-name.git

