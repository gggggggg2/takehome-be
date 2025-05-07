# Bungalow Take Home Project for Backend Developer Role

## About This Project
This is a Django based assignment. We have created a base project for you to work from. 
You are free to vary from our original base if you would like to. We provide it with the intention of providing 
a common base for all candidates to work from and to hopefully save you a bit of time. 

If you need an introduction to Django, their docs are an excellent place to start: https://docs.djangoproject.com/en/3.2

We encourage you to use the Django Rest Framework for developing your API. This is a framework that we use extensively 
at Bungalow, and it provides some nice functionality out of the box. https://www.django-rest-framework.org/

## What to Build
We would like you to build an API that can be used to query some information about houses.
Sample data is provided in the `sample-data` folder.
We have provided the stub for a Django command to import the data. Finish writing this code.
You should use Django's ORM to model the data and store it in a local database.
Then, utilize the Django Rest Framework to provide an API to query the models.
A very basic API design here would simply return all of the data available.
You can choose to improve and refine this very basic API design, and we encourage you to do so.
This will give us an opportunity to see how you approach API design.
If you are running out of time, you can outline how you would have done things differently given more time.


## How Will This Be Evaluated
We will use this project as our basis for our evaluation of your coding skill level as it relates to our team.
To do this, we will review your code with an eye for the following:

- Design Choices - choice of functionality, readability, maintainability, extendability, appropriate use of language/framework features
- Does it work as outlined
- Testing - have you considered how you'd test your code?
- Documentation - have you provided context around decisions and assumptions that you have made?
- Polish - have you produced something that would be ready to go into a production system?
  if not, have you clearly stated what would be needed to get from where it is to that level of polish?

## Time Expectations
We know you are busy and likely have other commitments in your life, so we don't want to take too much of your time.
We don't expect you to spend more than 2 hours working on this project. That being said, if you choose to put more or
less time into it for whatever reason, that is your choice. Feel free to indicate in your notes below if you worked on
this for a different amount of time and we will keep that in mind while evaluating the project. You can also provide us
with additional context if you would like to. Additionally, we have left a spot below for you to note. If you have ideas 
for pieces that you would have done differently or additional things you would have implemented if you had more time, 
you can indicate those in your notes below as well, and we will use those as part of the evaluation. For example, if you 
would have tested more, you can describe the tests that you would have written, and just provide 1 or 2 actual implemented
tests.

## Public Forks
We encourage you to try this project without looking at the solutions others may have posted. This will give the most
honest representation of your abilities and skills. However, we also recognize that day-to-day programming often involves 
looking at solutions others have provided and iterating on them. Being able to pick out the best parts and truly 
understand them well enough to make good choices about what to copy and what to pass on by is a skill in and of itself. 
As such, if you do end up referencing someone else's work and building upon it, we ask that you note that as a comment. 
Provide a link to the source so we can see the original work and any modifications that you chose to make. 

## Setup Instructions
1. Fork this repository and clone to your local environment. If you make your fork private, please give access to the `bungalow-engineering` user. 
1. Install a version of Python 3 if you do not already have one. We recommend Python 3.8 or newer.
1. You can use the built-in virtual environment creation within Python to create a sandboxed set of package installs. 
   If you already have a preferred method of virtualenv creation, feel free to proceed with your own method. 
   `python -m venv env`    
1. You will need to activate your virtual environment each time you want to work on your project. 
   Run the `activate` script within the `env/bin` folder that was generated.
1. We have provided a `requirements.txt` file you can use to install the necessary packages.
   With your virtualenv activated run: `pip install -r requirements.txt`
1. To run the django server run `python manage.py runserver`
1. To run the data import command run `python manage.py import_house_data`
1. You are now setup and ready to start coding. 


# Your Notes

## System Configuration
- Python: Python 3.13
- IDE used: PyCharm
- Database: Postgres 17

## Design
APIs were created to query and retrieve data from the listings table. 

This system implements the following API endpoints:

- /listings/<str:zillow_str>/
  - returns the listing with the specified id, or an error
  - example: 
    

- /query
  - this endpoint allows the caller to specify one or more field values to retrieve.
  - these values can either be a range (by specifying the desired range in json), or a specific value
  - examples:
    - http://127.0.0.1:8000/api/query?bathrooms={"gt": 1, "lt": 4}&bedrooms={"gt": 1, "lt": 5}
    - http://127.0.0.1:8000/api/query?bathrooms={"gt": 1, "lt": 4}&bedrooms=4
    - https://127.0.0.1:8000/api/query?bathrooms={"gt": 1, "lt": 4}&bedrooms={"gt": 1, "lt": 4}&rentzestimate_amount={"gt": 1000, "lt": 2000}
  

- /listings
  - this endpoint returns all available listings
  
## Additional tools used
- Postman for API testing.
- black for formatting
- flake8 for linting

## Time Spent
*Give us a rough estimate of the time you spent working on this. If you spent time learning in order to do this project please feel free to let us know that too.*
*This makes sure that we are evaluating your work fairly and in context. It also gives us the opportunity to learn and adjust our process if needed.*

I have been using Python, but not Django, so I spent extra time reading the Django and Django REST framework documentation, configuring my IDE, 
and taking some time to experiment with Django.  With this extra time, I exceeded the initial time limits for the project by a couple of hours.

## Assumptions
*Did you find yourself needing to make assumptions to finish this?*
*If so, what were they and how did they impact your design/code?*

I implemented APIs for a client, but did not build a front-end UI.  The API was designed so that it would work with a browser/javascript client.


## Next Steps
*Provide us with some notes about what you would do next if you had more time.* 
*Are there additional features that you would want to add? Specific improvements to your code you would make?*

This system works as a toy system, but is missing many features that would be needed by a production 
system (see following section below).

Possible next steps include:
- building APIs to allow for CRUD operations 
  - the CSV file only has 'zestimated' rental prices, but not actual rental prices.  There will likely need to be
  a way for this information to be collected and updated.
- restricting which fields should be query-able.  It depends on the use case, but end users looking for rental properties 
will not have access to all of the available fields.

### Anything else needed to make this production ready?
Yes! There are multiple changes that should be made for production use:
- Logging.  
  - Instead of logging output to the console or log file, a more advanced logging mechanism 
  could be implemented based on log severity.  Logs could also be sent to a centralized logging/analysis system.

  - DB operations can be logged to a different mechanism so the number, type, and response time of each query can be
  analyzed.  Doing this from the client can be useful in addition to DB-side analytics.


- Caching
It is likely that much of the traffic will be for retrieval of listing data.  If so, Redis (or something similar) 
can be used to offload queries from the database.


- Content
If this data is supplied from Zillow, it should be possible to retrieve images from Zillow, and make those available to the user.
Ideally these images would be stored on the appropriate CDN (S3 -> Cloudfront).


- Data validation: Address and zipcode validation could be added.  There are 3rd party libraries that will check to see if a mailing
address exits or not, and also whether the city/state/zip is valid.  
  - Also, zipcodes are treated as a string, not an integer.  This allows future support of Canadian or non-digit postal codes in the future, 
  and most zipcode operations can be performed as strings.
  - Support could also be added for additional date string formats (different separators, different day/month/year order)


- Data usage and DB indexing: I added a unique index to the listings.zillow_id field, as that is likely to be a common way data is retrieved and should
be unique per property.

  - However, based on fields that are searchable by users, other fields can also have indices so that searches don't perform 
  table scans (# bedrooms/bathrooms, home size, and rent are likely options for this).
  - Likewise, this system currently returns all of the available fields to the client, and assumes the client will 
  display those that are needed.  This isn't a good approach for a real system; for a production system we would want 
  to know which fields the user will be using (and this could differ based on what role & permissions the user has), 
  which they are allowed to see, and restrict the list of fields accordingly.
  - The Listings table was also created based on the csv file, but doesn't have fields to track its status (active, rented, unavailable)
  although these could be added to other tables to join against this table depending on the usage needs.


- Authentication
There is currently no authentication mechanism in place.  Ideally an API key, or some sort of user authentication scheme
should be used.


- Security: database params are currently stored in settings.py.  In a production environment, these should be stored externally
  (definitely not in plain text in a committed file!) with limited access.  One option is to store these using ENV variables,
these are easy to use locally, and work well with most deployment systems (and can be used with AWS Secrets Manager / AWS Parameter Store/)


- CORS support was not added, but if browser clients are to be used, this will need to be added.


- Interaction with other tables: who is renting this property?  who is the owner?  what is the contact info?  what amenities are available?  etc.

### Testing
Unit tests were created and run for this project.  To execute:
>python manage.py test



## How to Use

Migrations:
> python manage.py makemigrations api
>
> python manage.py migrate api 
> 
> python manage.py import_house_data /<path to csv>/data.csv

Unit tests:
> python manage.py test

Running server (can use whatever port is convenient)
> python manage.py runserver 8000