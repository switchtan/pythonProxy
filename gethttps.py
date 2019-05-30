import requests
import ssl
import urllib.request
ssl._create_default_https_context = ssl._create_unverified_context
response = urllib.request.urlopen('https://www.966seo.com')
print(response.read().decode('utf-8'))