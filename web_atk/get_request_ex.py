import urllib2

#body = urllib2.urlopen("http://wwww.nostarch.com")
url = "http://www.nostarch.com"
# body = urllib2.urlopen("http://www.yahoo.co.jp")
# print body.read()

headers = {}
headers['User-Agent'] = "Googlebot"

request = urllib2.Request(url, headers = headers)
response = urllib2.urlopen(request)

print response.read()

response.close()
