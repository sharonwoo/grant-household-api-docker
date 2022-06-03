# Household & Grant API 

Setup instructions after cloning the repo:

```
docker-compose build
docker-compose up
```

This project uses stock Django (db: SQLite) and django-rest-framework. It's my first completed non-tutorial project in Django (૭ ｡•̀ ᵕ •́｡ )૭

Go to http://localhost:8009/ ... but only api/v2/grants-public will be visible until authenticated.

**Superuser credentials are `admin` and `password` respectively.**

This will unlock the rest of the endpoints which are gated by authentication ... I couldn't really think of a better way to protect the data than that. 

The v2 grants-public endpoint is meant to answer the core requirement of `build up a list of recipients and which households qualify for it`, it's literally a list of households and family members without any other data exposed. It does take all combinations of `household_income` (integer), `married` (boolean), `age_less_than` (integer) and `age_more_than` (integer) though.

The v1 endpoints show all data and require a login to be accessed.


## Endpoints

```
api/v1/households/
api/v1/households/<household_id>/
api/v1/family_members/
api/v1/grants/
api/v2/grants-public/
```

Don't forget to enter the username and password for v1 endpoints!

### Household and Family Members (requirements 1-4)
* `api/v1/households/`: GET lists all households, POST to create household
* `api/v1/households/<household_id>/` GET lists 1 household, DELETE will delete household
* `api/v1/family_members/` GET lists all family members, POST creates the family member, DELETE `api/v1/family_members/<family_member_id>/` will delete the family member. For spouses: 
    * Create the first spouse
    * Copy the UUID of the first spouse and enter it as a parameter when creating the second spouse
    * The `marital_status` field will update based on whether spouse contains a valid value -- what is entered may be different from the value retrieved from the API
    * Non-legal marriages (age below 21 and not between husband & wife) will return an error 
    * Spouses can, however, reside in different households 

### Grant List (requirement 5)
* `api/v1/grants/` and `api/v2/grants-public/`: Use GET with appropriate query parameters `household_income` (integer), `married` (boolean), `age_less_than` (integer) and `age_more_than` (integer).

Pagination is in place and set to 30. 

Testing was done in Postman/django-rest-framework's UI manually initially then I wrote some tests (see below).

## Tests

Model, serializer and tests have been written in pytest but I broke it when I Dockerised :( I chose pytest because it's part of production at work (use what you know, right?). If you must know what it looks like, check the development history below...

## Development History 

Because I didn't set this up right for Docker the first time ;A; 

https://github.com/sharonwoo/grant-household-api

## Requirements

https://docs.google.com/document/d/1YyOJyq460UM3j8EzQsFgR4_VRspXy_tcxv5HRfMthwg/

## Next Steps & Improvements

* Setup Postgres 
* Create seed data file and load data that way 
* Fix pytest and setup pytest-cov
* Setup black in container (formatting done locally with black)
* Explore documenting API with Swagger/CoreAPI
