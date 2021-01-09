from bs4 import BeautifulSoup
import requests
import json

headers = {
    "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
}

DATA_FILE_NAME = "Dishes.json"

# The dictionary dishes contains a key for each section
dishes = {}

# List of all the sections we will scrape
sections = ["paneer","breakfast","lunch","rice","snacks","sweets","sabzi","soup","salad"]
h=[] #stores the time for each dish
b=[]#stores the dishes where the time is not in the reqd format

# Go through the list of sections
for section in sections:
    print("")
    print("Processing section: ", section)

    # This is the list of all the recipes in this section
    dishes[section] = []

    with open(section + ".txt","r") as x:
        u=x.readlines()
        for URL in u:

            response = requests.get(URL, headers=headers)  #varLink
            card_soup = BeautifulSoup(response.content, "html.parser").find("div", {"class": "wprm-recipe wprm-recipe-template-columns-hk"})
            if not card_soup:
                print("Failed to load: ",URL)
                continue
            else:
                ## New empty recipe dictionary
                recipe = {}

                if(card_soup.find("h2", {"class": "wprm-recipe-name wprm-block-text-normal"}) != None):
                    recipe["name"] = card_soup.find("h2", {"class": "wprm-recipe-name wprm-block-text-normal"}).get_text().strip()
                else:
                    recipe["name"] = "NA"
                if( card_soup.find("span", {"class": "wprm-recipe-course wprm-block-text-uppercase"})!= None ):
                    recipe["course"] = card_soup.find("span", {"class": "wprm-recipe-course wprm-block-text-uppercase"}).get_text().title()
                else:
                    recipe["course"] = "NA"

                if( card_soup.find("span", {"class": "wprm-recipe-cuisine wprm-block-text-uppercase"}) != None):
                     recipe["cuisine"] = card_soup.find("span", {"class": "wprm-recipe-cuisine wprm-block-text-uppercase"}).get_text().title()
                else:
                     recipe["cuisine"] = "NA"

                if( card_soup.find("span", {"class": "wprm-recipe-servings-adjustable-text"}) != None):
                     recipe["servings"] = card_soup.find("span", {"class": "wprm-recipe-servings-adjustable-text"}).get_text().title()
                else:
                     recipe["servings"] = "NA"

                if( card_soup.find("span", {"class": "wprm-recipe-keyword wprm-block-text-uppercase"}) != None):
                     recipe["keywords"] = card_soup.find("span", {"class": "wprm-recipe-keyword wprm-block-text-uppercase"}).get_text().strip().title().split(" ")
                else:
                    recipe["keywords"] = "NA"

                if(card_soup.find("span", {"class": "wprm-recipe-nutrition-with-unit"}) != None):
                     recipe["calories"] = card_soup.find("span", {"class": "wprm-recipe-nutrition-with-unit"}).get_text().title()
                else:
                     recipe["calories"] = "NA"


                #time block
                if(card_soup.find("span", {"class": "wprm-recipe-time wprm-block-text-uppercase"})!= None ):
                    
                    total_time = card_soup.find("div", {"class": "wprm-recipe-block-container wprm-recipe-block-container-columns wprm-block-text-uppercase wprm-recipe-time-container wprm-recipe-total-time-container"})
                    if total_time:
                        total_time = total_time.find("span", {"class": "wprm-recipe-time wprm-block-text-uppercase"}).get_text()
                        v=str(total_time)
                        print(v)
                        print()
                        if v[3]=="m" or v[2:]=="m":
                            if v[1]==" ":
                                recipe["total_time"] = int(v[0])
                                h.append(int(v[0]))
                            else:
                                g=v[0:2]
                                recipe["total_time"] = int(g)
                                h.append(int(g))
                        elif(v[2]=="h"):
                            if(int(v[0])>1):
                                if len(v)>=9:
                                    if v[9]==" ":
                                        minutes=int(v[8])
                                        recipe["total_time"] = ((int(v[0])*60)+minutes)
                                        h.append((int(v[0])*60)+minutes)   
                                    else:
                                        recipe["total_time"] = ((int(v[0])*60)+ int(v[8:10]))
                                        h.append((int(v[0])*60)+ int(v[8:10]))
                                else:
                                    recipe["total_time"] = ((int(v[0])*60))
                                    h.append((int(v[0])*60))
                            else:
                                if len(v)>=8:
                                    if v[8]==" ":
                                        minutes=int(v[7])
                                        recipe["total_time"] = ((int(v[0])*60)+minutes)
                                        h.append((int(v[0])*60)+minutes)
                                    else:
                                        recipe["total_time"] = ((int(v[0])*60)+ int(v[7:9]))
                                        h.append((int(v[0])*60)+ int(v[7:9]))
                                else:
                                    recipe["total_time"] = ((int(v[0])*60))
                                    h.append((int(v[0])*60))
                        elif(v[3]=="h"):
                            if len(v)>=10:
                                if v[10]==" ":
                                    minutes=int(v[9])
                                    recipe["total_time"] = ((int(v[0:2])*60)+minutes)
                                    h.append((int(v[0:2])*60)+minutes) 
                                else:
                                    recipe["total_time"] = ((int(v[0:2])*60)+ int(v[9:11]))
                                    h.append((int(v[0])*60)+ int(v[9:11]))
                            else:
                                recipe["total_time"] = ((int(v[0:2])*60))
                                h.append((int(v[0])*60))
                        else:
                            recipe["total_time"]=0
                            b.append(recipe["name"])
                    else:
                        recipe["total_time"]=0
                        b.append(recipe["name"])
                else:
                    recipe["total_time"]=0
                    b.append(recipe["name"])
                    
                #Now get the ingredients
                print(recipe["total_time"])
                print()
                Ing = []
                response = requests.get(URL, headers=headers)  #varLink
                pagetext = BeautifulSoup(response.content, "html.parser")
                lists = pagetext.find_all("ul", class_="wprm-recipe-ingredients")
                for list in lists:
                    ingredients = list.find_all("li", class_="wprm-recipe-ingredient")
                    for ingredient in ingredients:
                        a = ingredient.find("span", class_="wprm-recipe-ingredient-amount")
                        U = ingredient.find("span", class_="wprm-recipe-ingredient-unit")
                        N = ingredient.find("span", class_="wprm-recipe-ingredient-name")
                        amount = ""
                        if a:
                            amount = str(a.get_text())
                        unit = ""
                        if U:
                            unit = str(U.get_text())
                        name = ""
                        if N:
                            name = str(N.get_text())
                        s=amount+" "+unit+" "+name
                        Ing.append(s)
                recipe["ingredients"] = Ing

                # Now get the instructions
                Inst = []
                lists = pagetext.find_all("ul", class_="wprm-recipe-instructions")
                for list in lists:
                    instructions = list.find_all("div", class_="wprm-recipe-instruction-text")
                    for instruction in instructions:
                        if instruction:
                            Inst.append(str(instruction.get_text()))
                recipe["instructions"] = Inst

                # Finally get the image URL
                recipe["image"] = ""
                metas = pagetext.find_all("meta")
                for meta in metas:
                    try:
                        if meta.attrs["property"] == "og:image":
                            recipe["image"] = meta.attrs["content"]
                            break
                    except:
                        # ignore the exception
                        do_nothing = True

                # Append this recipe to the list of recipes for the section
                dishes[section].append(recipe)
                if(recipe["total_time"]!=0):
                    print("Processed: ", recipe["name"],recipe["total_time"])
                    
                    
               

# All finished, so write the data as JSON
with open(DATA_FILE_NAME, "w") as data_file:
    json.dump(dishes, data_file, indent=4)







                                                                                    
