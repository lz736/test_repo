import urllib.request

response = urllib.request.urlopen("http://wwww.baidu.com")
print(response.read())