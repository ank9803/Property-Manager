# Property Manager

This Repo contains Graphql mutation for fetch NYC Real Estate Assessment Property data and Saves into DB and queries to read data.

## Setup

To use this project, run this commands:

1. Clone the repository.
2. Create a virtual environment to install dependencies in and activate it.
   `virtualenv env`
   `source env/bin/activate`
3. Then install the dependencies from requirements.txt.
   `pip install -r requirements.txt`
4. Navigate to project folder and start server.
   `cd propertymanager`
   `python manage.py runserver`
5. And navigate to `http://127.0.0.1:8000/graphql/`

### Explnation

I’ve created graphql mutation with 2 arguments, zip code and address which fetches and parses building data from NYC properties assessments dataset and saves it to DB.

The dataset doesn’t have a specific address field, so to match the address

- I’ve used housenum_lo and street_name fields from dataset
- The address will be space or comma separated with house number, street name, and state respectively i.e Address: 445 5th Ave NY, 400 W 37th St, New York, NY
  - Where 1st number is considered as the house number
  - If the state name is given “NY” or “New York”, it’ll be removed
  - And the remained text will be the street name
- I’ve removed "English Ordinal Suffix" from the street name because the data set doesn’t have it
  - For example
    - “W 37th St “will be “W 37 St”
    - “5th Ave” will be “5 Ave”
- If the street name contains any abbreviations for direction point ex: E, W, or S then it’ll be matched with “E%” LIKE operator
