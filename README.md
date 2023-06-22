
# SocialMedia API

The Social Media API is a powerful and efficient RESTful API built using FastAPI framework that provides developers with a set of endpoints to interact with social media data. It allows users to perform various operations, including creating posts, retrieving posts, following other users, and more. This README provides an overview of the project, installation instructions, API documentation, and usage examples.




## Features

- HTTP request: This API uses HTTP GET, POST, PUT and DELETE request according to action you want to perform.
- HTTP Exception: HTTP response status code according to request you'll recive response.Some response code are 200, 201,401, 403, 404 etc.
- Pydantic: FastAPI uses pydantic for Data validation and settings management using python type annotations.
- OAuth2: For authentication purposes i've utilized Oauth2 to take email id password as parameters. Once the user created the password is hashed so even if our database compromized nothing could be done with that information.FastAPI also provide Jose to generate JWT tokens. 
- SQLAlchemy: SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.With SQLAlchemy using OOPs we can define database models. The FastAPISessionMaker class provides an esaily-customized SQL- Alcheny Session dependency.





## Installation

Install my-project with npm

```bash
  npm install my-project
  cd my-project
```
Run the python file after setting the virtual env.
    


