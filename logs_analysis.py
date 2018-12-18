#!/usr/bin/env python
# -*- coding: utf-8 -*-

# importing required libraries

import psycopg2
from flask import Flask, request


app = Flask(__name__)


# 1st Answer

DBNAME = "news"

db = psycopg2.connect(database=DBNAME)
c = db.cursor()
c.execute("select title, count(*) as views"
          " from articles join log on articles.slug = substring(log.path, 10)"
          " and log.status = '200 OK' group by articles.title"
          " order by views desc limit 3;")

answer1 = c.fetchall()


# 2nd Answer

c.execute("select name, count(*) as views"
          " from (authors join articles on authors.id=articles.author)"
          " join log on articles.slug = substring(log.path, 10)"
          " group by name order by views desc;")

answer2 = c.fetchall()


# 3rd Answer

c.execute("select day, (misses*100/percent) as percentage"
          " from allrequests join miss on allrequests.day=miss.miss_day"
          " where misses*100/percent > 1;")

answer3 = c.fetchall()

db.close()

# HTML template with placeholders inserted

HTML_WRAP = '''
<!DOCTYPE html>
<html>
  <head>
    <title>Log Analysis</title>
    <style>
      h1{ text-align: center; }
    </style>
  </head>
  <body>
    <h1>Log Analysis Report:</h1><br>
  <h3>What are the most popular three articles of all time?</h3>
    <table>
    <tr>
      <th>Articles</th>
      <th>No. of Views</th>
    </tr>
    <tr>
     <td><strong>%s</strong></td>
     <td align="center"><emphasis>%s</emphasis></td
    </tr>
    <tr>
     <td><strong>%s</strong></td>
     <td align="center"><emphasis>%s</emphasis></td
    </tr>
    <tr>
     <td><strong>%s</strong></td>
     <td align="center"><emphasis>%s</emphasis></td
    </tr>
    </table>
    <h3>Who are the most popular article authors of all time?</h3>
    <table>
    <tr>
      <th>Authors</th>
      <th>Aggregate Views</th>
    </tr>
    <tr>
     <td><strong>%s</strong></td>
     <td align="center"><emphasis>%s</emphasis></td
    </tr>
    <tr>
     <td><strong>%s</strong></td>
     <td align="center"><emphasis>%s</emphasis></td
    </tr>
    <tr>
     <td><strong>%s</strong></td>
     <td align="center"><emphasis>%s</emphasis></td
    </tr>
    <tr>
     <td><strong>%s</strong></td>
     <td align="center"><emphasis>%s</emphasis></td
    </tr>
    </table>
    <h3>On which days did more than 1 percent of requests lead to errors?</h3>
    <table>
    <tr>
      <th>Day</th>
      <th>Miss Percentage</th>
    </tr>
    <tr>
      <td><strong>%s</strong></td>
      <td align="center"><emphasis>\t%s</emphasis></td
    </tr>
    </table>
  </body>
</html>
'''

# routing handler with a default function,
# that populates data from queries in HTML template


@app.route('/')
def results():
    html = HTML_WRAP % (answer1[0][0], answer1[0][1], answer1[1][0],
                        answer1[1][1], answer1[2][0], answer1[2][1],
                        answer2[0][0], answer2[0][1], answer2[1][0],
                        answer2[1][1], answer2[2][0], answer2[2][1],
                        answer2[3][0], answer2[3][1], answer3[0][0],
                        (answer3[0][1]))
    return html


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

