# newsdata.py
---
newsdata.py is  python script which extracts data from a PostgreSQL database using the `psycopg2` python module. It was created to illustrate my working knowledge of SQL database structure, commands and syntax.

# Quickstart
---
### Database Installation & Setup (Linux)

`$ sudo apt-get install postgresql`

1. Download zip file: [Download File Here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

2. Unzip file then `cd` into the directory and run the following:

 * `$ CREATE DATABASE news`
 * `$ psql -d news -f newsdata.sql`


3. Create the following VIEWS in the news database

  * `CREATE VIEW author_views AS SELECT author, count(*) AS num FROM articles JOIN log ON log.path LIKE '%' || articles.slug || '%' WHERE status = '200 OK' GROUP by author ORDER by num desc;`

  * `CREATE VIEW error AS SELECT date(time), count(*) AS not_found FROM log WHERE status = '404 NOT FOUND' GROUP by date; `

  * `CREATE VIEW success AS SELECT date(time), count(*) AS ok FROM log WHERE status = '200 OK' GROUP by date;`

  * `CREATE VIEW date_status AS SELECT success.date, ok, not_found FROM success JOIN error on success.date = error.date;`

  * `CREATE VIEW errors_per_day AS SELECT date, (cast(not_found as float)/ok) * 100 as percent_errors from date_status;`


### Run the Queries
`$ python newsdata.py`

newsdata.py was designed to extract the following:

1. Most popular 3 articles of all time based on views
2. Most popular author of all time based on views
3. Days where greater than 1% of request led to errors

## License
___
[CC-BY](https://creativecommons.org/licenses/by/3.0/)
