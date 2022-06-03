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

## Assumptions

## End users & endpoint design
* End-user of v2 endpoint `api/v2/grants-public/`: 
    * users who are required to administer a list of households and qualifying family members, for example for grant distribution
    * endpoint serves a front-end which will input the query parameters for the 5 grants given 
    * Format of endpoint: 
        * data in "results"; the first uuid is household-level
        * other fields are due to pagination

```
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "uuid": "6c9095b2-a69e-4897-af2c-a07235bb842b",
            "family_members": [
                {
                    "uuid": "98859210-1f22-46e6-9f21-3ce179899050"
                },
                {
                    "uuid": "79ed4cbf-a342-47cd-adce-d05d7c1bdfb2"
                },
                {
                    "uuid": "d439cfa1-db92-4862-9efe-6946bc74d1e1"
                }
            ]
        }, 
        ...
```

* End-user of v1 endpoints: 
    * superusers who have credentials to view sensitive data and process it to drive management decisions, e.g. in response to requests on how many households would be impacted by a given grant, the distribution of household demographics such as income, age
    * would be good to ingest data to serve a private front end such as a Tableau dashboard (data pipeline and front end not covered by our test)
    * Format: 
        * Spouse ID appears as a primary key

```
 {
            "uuid": "6c9095b2-a69e-4897-af2c-a07235bb842b",
            "housing_type": "HDB",
            "family_members": [
                {
                    "uuid": "98859210-1f22-46e6-9f21-3ce179899050",
                    "household": "6c9095b2-a69e-4897-af2c-a07235bb842b",
                    "name": "Name 1",
                    "gender": "Male",
                    "marital_status": "Married",
                    "spouse": "79ed4cbf-a342-47cd-adce-d05d7c1bdfb2",
                    "occupation_type": "Employed",
                    "annual_income": 35000,
                    "date_of_birth": "1987-01-01"
                },
    ... ]
    ... }
```
Reasoning: 
* Requirement given states for grant endpoint to accept search parameters and return results based on 5 grant schemes: 
    * Student Encouragement Bonus: Households and qualifying members children <16 years and income <$100k
        * Expected behaviour: Grant endpoints return list of {household_id, family_members: [list of students_that_qualify]}
    * Family Togetherness Scheme: Husband + wife, children of younger than 18
        * Expected behaviour: Grant endpoints return list of {household_id, family_members: [husband, wife, and list of any children]}
        * As marriage is illegal in our API below 21, the minimum household size returned is 3
    * Elder Bonus and Baby Sunshine Grant: >50 years and <5 years of age respectively
        * Elder Bonus expected behaviour: Grant endpoints return list of {household_id, family_members: [qualified elders]}
        * Baby Sunshine Grant expected behaviour: Grant endpoints return list of {household_id, family_members: [qualified babies]}
    * YOLO GST Grant: households of annual income <$100k
        * Expected behaviour: Grant endpoints return list of {household_id, family_members: [all household members]} in households of less than 100k annual income 
* **Returning 1 view for each grant, which would probably be the safest to pass to administrative end users, would safeguard information but contradicts requirement 5a which asks for search parameters AND the ability to return the above grant results**. Search parameters would be meaningless if the grant endpoint didn't return anything outside of inputs valid for the above grants... and I imagine also frustrating for anyone hitting the endpoint / maintaining it with updates for whenever the grant conditions change. Resolution for data privacy is a public-facing endpoint that only has UUIDs (v2), and everything else gated behind authentication 


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

Model, serializer and view tests have been written in pytest but I broke it when I Dockerised :( I chose pytest because it's part of production at work (use what you know, right?). If you must know what it looks like, check the development history below...

## Development History 

Because I didn't set this up right for Docker the first time ;A; 

https://github.com/sharonwoo/grant-household-api

## Requirements

https://docs.google.com/document/d/1YyOJyq460UM3j8EzQsFgR4_VRspXy_tcxv5HRfMthwg/

## Next Steps & Improvements

* Setup Postgres 
* Create seed data file and load data that way 
* Fix pytest and setup pytest-cov
* Integrate factory_boy in tests 
* Setup black in container (formatting done locally with black)
* Explore documenting API with Swagger/CoreAPI
