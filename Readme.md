# Household & Grant API 

Setup instructions after cloning the repo:

```
docker-compose build
docker-compose up
```

This project uses stock Django (db: SQLite) and django-rest-framework. It's my first completed non-tutorial project in Django (૭ ｡•̀ ᵕ •́｡ )૭

Go to http://localhost:8009/ ... but only api/v2/grants-public is visible.

Superuser credentials are `admin` and `password` respectively.

This will unlock the rest of the endpoints which are gated by authentication ... I couldn't really think of a better way to protect the data than that. 

The v2 grants-public endpoint is meant to answer the core requirement of `build up a list of recipients and which households qualify for it`, it's literally a list of households and family members without any other data exposed. It does take all combinations of `household_income` (integer), `married` (boolean), `age_less_than` (integer) and `age_more_than` (integer) though.

The v1 endpoints show all data and require a login to be accessed.


## Endpoints

```
api/v1/grants/
api/v1/households/<household_id>/
api/v1/family_members/
api/v1/grants/
api/v2/grants-public/
```

## Tests

Model, serializer and tests have been written in pytest but I broke it when I Dockerised :( I chose pytest because it's part of production at work (use what you know, right?).

## Development History 

Because I didn't set this up right for Docker the first time ;A; 

https://github.com/sharonwoo/grant-household-api

## Requirements

https://docs.google.com/document/d/1YyOJyq460UM3j8EzQsFgR4_VRspXy_tcxv5HRfMthwg/

## Next Steps

* Setup Postgres 
