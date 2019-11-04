# jamtech-api

## Installation Instructions

- `git clone https://github.com/Robo-romeski/jamtech-api.git`
- `cd jamtech-api`
- `pip3 install virtualenv`
- `virtualenv env`
- `source env/bin/activate`
- `pip3 install -r reqs.txt`
- `python3 manage.py makemigrations`
- `python3 manage.py migrate`
- `python3 manage.py runserver`

## How to run server
- `source env/bin/activate`
- `python3 manage.py runserver`

## Live link
[jamtech-api-ebs](http://jamtech-django-env.8yzvisztqt.us-east-1.elasticbeanstalk.com/)


## Pagination Instructions
Example Request URL:
`GET https://api.example.org/users/?page=4`

Example Response:
`
HTTP 200 OK
{
    "count": 1023
    "next": "https://api.example.org/users/?page=5",
    "previous": "https://api.example.org/users/?page=3",
    "results": [
       …
    ]
}
`

## Filter Instructions
Below are the queryable properties for business profiles:
- company_name
- industry_category
- industry_segment
- experience_level
- recent_project
- work_seeking
- summary
- zipcode

To filter for a property, use a GET parameter, similar to pagination above.
`GET https://api.example.org/users/profiles/?zipcode=11221`
