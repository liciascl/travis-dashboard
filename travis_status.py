import urllib.request as requests
from bs4 import BeautifulSoup
import time

groups = dict()
#Colocar /export?format=csv no final da url
csv_file = "https://docs.google.com/spreadsheets/d/1oK-7ITXBQ40BhHO-izAtLTZBzcwrWoWWmYKwCIP9Z_g/export?format=csv"
response = requests.urlopen(csv_file)
html_csv = response.read().decode("utf-8") 
html_csv = html_csv.split("\r\n")



html_csv = html_csv[1:] #Retira a Primeira linha da tabela
start_time = time.time()

for lines in html_csv:
    words = []
    a = lines.split(",")
    groups[a[0]] = {}
    if a[1][-1] == "/":
        a[1] = a[1][:-1]
    link = "https://travis-ci.org" +  a[1].split("github.com")[1] +".svg?branch=master"
    groups[a[0]]["link"] = link
    
    response = requests.urlopen(groups[a[0]]["link"])
    html = response.read()
    soup = BeautifulSoup(html, features="html5lib")
    for text_tags in soup.find_all('text'):
        if str(text_tags.text) not in words:
            words.append(str(text_tags.text))

    groups[a[0]]["words"] = words


if(len(groups)>0):
    print (groups)
    print (str((time.time() - start_time)/len(groups)) + " " + "segundo(s) por request")
