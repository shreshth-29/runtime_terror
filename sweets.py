from bs4 import BeautifulSoup
import requests
import json
with open("sweets.txt", "a") as myfile:
    
    URL="https://hebbarskitchen.com/recipes/indian-sweets-recipes/"
    i=1
    while i<=14:
        if(i==1):
            response = requests.get(URL)
            pagetext = BeautifulSoup(response.content, "html.parser")
            links = pagetext.find_all(class_="td-module-thumb")
            for link in links:
                ref = link.find("a")
                myfile.write(ref["href"] +"\n")
                print(ref["href"])
            i+=1
        else:
            response = requests.get(URL+"page/"+str(i)+"/")
            i+=1
            pagetext = BeautifulSoup(response.content, "html.parser")
            links = pagetext.find_all(class_="td-module-thumb")
            for link in links:
                ref = link.find("a")
                myfile.write(ref["href"] +"\n")
                print(ref["href"])
            i+=1
