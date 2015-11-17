__author__ = 'nicolasbortolotti'

import sys
import csv
import argparse

from oauth2client import client
from apiclient import sample_tools

argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument("-p", "--parameters", nargs='+', type=str, default=["android", "polymer"], help="adding parameters")

def main(argv):
  people = raw_input('G+ id to analyze?: ')
  postnumers = int(raw_input('number of posts: '))

  service, flags = sample_tools.init(
      argv, 'plus', 'v1', __doc__, __file__, parents=[argparser],
      scope='https://www.googleapis.com/auth/plus.me')

  try:
    person = service.people().get(userId=people).execute()
    # show people name
    print 'ID: %s' % person['displayName']
    tech = flags.parameters
    print 'Parameters used: %s' % tech

    request = service.activities().list(userId=person['id'], collection='public', maxResults='1')
    #open file
    myfile = open(people + '.csv', 'wb')

    try:
        writer = csv.writer(myfile)
        writer.writerow(('id', 'content', 'tests', 'replies', 'plusoners', 'resharers'))

        # Information from activities
        count = 0
        while (count < postnumers):
            activities_document = request.execute()
            if 'items' in activities_document:
                for activity in activities_document['items']:
                    id =activity['id']
                    content = activity['object']['content'].encode("utf-8")
                    test = any(x in content.split() for x in tech)
                    replies =activity['object']['replies']['totalItems']
                    plusoners =activity['object']['plusoners']['totalItems']
                    resharers = activity['object']['resharers']['totalItems']

                    writer.writerow((id, content, test ,replies, plusoners, resharers))
            count = count + 1
            request = service.activities().list_next(request, activities_document)
    finally:
            myfile.close()

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired')

if __name__ == '__main__':
  main(sys.argv)
