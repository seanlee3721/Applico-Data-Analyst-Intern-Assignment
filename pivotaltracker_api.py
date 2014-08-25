##coding=utf8
##date=2014-08-24
##author=Baichen Li

import urllib2
import cookielib
import json
from datetime import datetime
import pprint

def get_html(url):
    '''Attach token, get http json response
    INPUT: url
    OUTPUT: http response
    '''
    cookies = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
    headers = {'X-TrackerToken': '0a1021e3dce4529136474517da486062'} # add token
    req = urllib2.Request(url, None, headers)
    res = opener.open(req)
    return res.read()

def projectURL(ID):
    '''Generate data url
    '''
    return "https://www.pivotaltracker.com/services/v5/projects/%s/stories" % ID

def num_of_story(jdata):
    '''Return how many stories in project
    '''
    counter = 0
    for entry in jdata:
        if entry['kind'] == 'story':
            counter +=1
    return counter

def main():
    '''Sometime the internet may be suck, so you can comment following 2 lines
    and uncomment the next 2 lines. Because I saved the json response as a "api_response.txt"
    '''
    # url = projectURL('1151258') # = https://www.pivotaltracker.com/services/v5/projects/1151258/stories
    # html = get_html(url)
    
    '''If real-time api access not working, use local file
    '''
    with open('api_response.txt', 'rb') as f:
        html = f.read()
    
    ''' test '''
    print 'http response = \n%s' % html
    jdata = json.loads(html) # load txt data to json
    
    print 'how many story in this project = %s' % num_of_story(jdata) # print how many entries are story
    
    results = list() # generate the data we need
    for entry in jdata:
        if entry['kind'] == 'story': # make sure it's a story
            dt = datetime.strptime(entry['accepted_at'], '%Y-%m-%dT07:00:00Z') # strip time format string
            results.append( (dt, entry['estimate'] ) )
    
    pprint.pprint( results ) # pretty display
    
    ''' === If you cannot run this scripts, the expected result should be: 
    pprint.pprint( results ) = 
    [(datetime.datetime(2014, 7, 18, 0, 0), 8),
     (datetime.datetime(2014, 7, 25, 0, 0), 4),
     (datetime.datetime(2014, 8, 1, 0, 0), 2),
     (datetime.datetime(2014, 8, 8, 0, 0), 4),
     (datetime.datetime(2014, 8, 15, 0, 0), 2)]
    
    Thus the BurnDown Chart looks like:
    week0 Budget Consumed, Complexity Points Remaining = 0, 20
    week1 Budget Consumed, Complexity Points Remaining = 1000, 12
    week2 Budget Consumed, Complexity Points Remaining = 3000, 8
    week3 Budget Consumed, Complexity Points Remaining = 4000, 6
    week4 Budget Consumed, Complexity Points Remaining = 6000, 2
    week5 Budget Consumed, Complexity Points Remaining = 9000, 0
    '''
    
if __name__ == '__main__':
    main()