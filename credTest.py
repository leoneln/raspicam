import os
from google.cloud import bigquery
##Cred test works with but only when os is imported and environ defined here.
#gues we could try to define as global..
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../zippy-avatar.json'


def query_stackoverflow():
    client = bigquery.Client()
    query_job = client.query("""
        SELECT
          CONCAT(
            'https://stackoverflow.com/questions/',
            CAST(id as STRING)) as url,
          view_count
        FROM `bigquery-public-data.stackoverflow.posts_questions`
        WHERE tags like '%google-bigquery%'
        ORDER BY view_count DESC
        LIMIT 10""")

    results = query_job.result()  # Waits for job to complete.

    for row in results:
        print("{} : {} views".format(row.url, row.view_count))


if __name__ == '__main__':
    query_stackoverflow()