__author__ = 'nicolasbortolotti'

import sys

from oauth2client import client
from apiclient import sample_tools

def main(argv):
  service, flags = sample_tools.init(
      argv, 'plus', 'v1', __doc__, __file__,
      scope='https://www.googleapis.com/auth/plus.me')


  try:
    person = service.people().get(userId='me').execute()

    print 'ID: %s' % person['displayName']
    print
    print '%-040s -> %s' % ('[Activitity ID]', '[Content]')

    # Don't execute the request until we reach the paging loop below.
    request = service.activities().list(userId=person['id'], collection='public', maxResults='10')

    # Loop over every activity and print the ID and a short snippet of content.
    #while request is not None:
    #  activities_doc = request.execute()
    #   for item in activities_doc.get('items', []):
    #     print '%-040s -> %s' % (item['id'], item['object']['content'][:30])

    #  request = service.activities().list_next(request, activities_doc)

    while request != None:
      activities_document = request.execute()
      if 'items' in activities_document:
          print 'got page with %d' % len( activities_document['items'] )
          for activity in activities_document['items']:
            print activity['id'], activity['object']['content'][:15], activity['object']['plusoners']['totalItems']

      request = service.activities().list_next(request, activities_document)

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired')

if __name__ == '__main__':
  main(sys.argv)