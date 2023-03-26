## BUY-ME-A-GIFT
#### Vinhood wants to create a new service for customers to add their favorite products to a wishlist, and the name of the service is BUY-ME-A-GIFT.

#### The following points are the product manager's requirements for the IT team.
#### The service should allow authenticated users to create a product, product_category
### User:
*  The user should be able to sign-up and sign in with an email address and password
*  The user should be able to reset the password.
*  The user has a unique identifier
*  The unique identifier only can be read
*  The user has a wish-list that can add only one product from each product category.
*  The user can add multiple product at one request
### Product:
*  The product has a name, price (including currency), rank, product_category, created_time, updated_time
*  The product can have only one product category
*  The created_time only can be read
*  The updated_time only can be written

### Product Category:
*  The product category has only a name

### Information about endpoints:
*  The user should be able to create, update, delete, list, and retrieve a product
*  The retrieve and list actions are also available for unauthenticated users
*  In the case of the list, the endpoint should only show the name, price, product category, created_time
*  The list endpoint should accept price_gt, and price_lt as query strings of the view
*  An endpoint to add/remove products to the wish-list only for authenticated users
*  The endpoint to list wish-listed products accessible by an unauthenticated user base on a unique identifier of the user
*  The endpoint should be able to sort the products based on rank and/or created_time.
*  The Authenticated user can only create and remove the product categories.

### Technical requirements from the IT team:
* Use DRF 3.14.X
* Use Pipenv as ENV management tools
* Write docker-compose file for Postgres database and REST-API
* Use the ENV variables for the configuration of the docker-compose, docker, and Django
* Use JWT authentications
* Follow the TDD and write unit tests for all aspects of the MVC paradigm
    * Use the client in DRF for end-to-end testing
* Provide swagger documentation for the endpoints
* At least document one of the modules with pep-257 style
* Use MyPy for type-checking and provide types for all the functions and variables