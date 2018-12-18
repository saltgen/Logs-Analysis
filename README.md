#  Project: Logs Analysis

- This project has been created to aggregate and reveal reports on authors and how their articles are performing
in the open world.

- The last query also performs a health check on the website infrastructure itself by finding the percentage of
 miss.

## Design

1. The first query was created to rank the best perfoming articles, according to their views.
   The query was created by aggregatng the result on joining 'articles' and 'log' tables on basis of 'slug' and portion of the 'path' values.
2. The second query was created by aggregating author id in authors and article, against the log table which showed how many articles were popular per author.
3. For the third query two views were created as provided at the end. The first one, 'allrequests' was a sum of requests for each day and the second one, misses was the sum of 'misses' by each day. A miss percentage was calculated out of the view by aggregatiing them on the dates. Only the one(s) above 1% needed to be displayed
4. The fourth task was to display the data from the queries on a non-interactive webpage in proper format. This was done with the help of Flask by executing the SQL statements and substituting the values from the same.

## Prerequisites

- Web Browser

- Python2

- psycopg2 (Utility required to connect to PostgreSQL database)

- Flask(Python Web Framework)

- Postgresql

- This project is almost completely based on database queries. Please make sure that PostgreSQL is properly installed on your computer. 
- Download the database dump 'newsdata.sql', https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
- Execute 'psql -d news -f newsdata.sql' on the psql prompt then connect to the database news using '\c news'

- Custom Views
- The sql queries provided below under **Views**, need to be executed on local database for the output

**Running the project**

-There is no need to install this project, the log_analysis.py file needs to be run using Python. If all prerequisites are met then a localhost url wil appear on the terminal. The same needs to be visited on a browser.

**Acknowledgments**

- My instructors at Udacity
- Udacity chapters on particularly views, joins & aggregations. I found myself checking these topics, frequently.
- W3Schools for basic html structures and semantics
- PostgreSQL documentation: https://www.postgresql.org/docs/
- Thanks to PurpleBooth(https://gist.github.com/PurpleBooth) for her README template,

**Views**

Implemented for obtaining total hits on the articles per day,

```sh
create view allrequests as 
select left(cast(time as varchar), 10) as day, count(*) as percent 
from log group by day;
```

Implemented for obtaining total misses on the articles per day,

```sh
create view miss as 
select left(cast(time as varchar), 10) as miss_day, count(*) as misses 
from log where log.status != '200 OK' 
'''
group by miss_day;
