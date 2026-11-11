from recipe_scrapers import scrape_me
import csv
import datetime
import unicodedata

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.length = 0

    def enqueue(self, element):
        new_node = Node(element)
        if self.rear is None:
            self.front = self.rear = new_node
            self.length += 1
            return
        self.rear.next = new_node
        self.rear = new_node
        self.length += 1

    def dequeue(self):
        if self.isEmpty():
            return "Queue is empty"
        temp = self.front
        self.front = temp.next
        self.length -= 1
        if self.front is None:
            self.rear = None
        return temp.data

    def peek(self):
        if self.isEmpty():
            return "Queue is empty"
        return self.front.data

    def isEmpty(self):
        return self.length == 0

    def size(self):
        return self.length

    def printQueue(self):
        temp = self.front
        while temp:
            print(temp.data, end=" -> ")
            temp = temp.next
        print()


dataset = {"rice| cooked| for serving", "fresh cilantro| chopped| for garnish"}
linqueue = Queue()
linkset={"https://tasty.co/recipe/easy-peasy-potato-curry"}
linqueue.enqueue("https://tasty.co/recipe/easy-peasy-potato-curry")
bad_data={"/recipe/marry-me-chicken-oven-baked-risotto", "/recipe/fire-enoki-mushrooms", "/recipe/butter-chicken-stuffed-shell-pasta", "/recipe/ries-yakisoba"}

for i in range(1,151):
    if (linqueue.isEmpty()):
        break
    
    try:
        scraper = scrape_me(linqueue.dequeue())
    except FillPluginException:
        continue
    
    for ingredient in scraper.ingredients():
        nfkc_str = unicodedata.normalize('NFKC', ingredient)
        nfkc_str.replace(unicodedata.lookup('FRACTION SLASH'), unicodedata.lookup("SOLIDUS"))
        dataset.add(nfkc_str)
    newlinks={*()}
    for link in scraper.links():
        if link["href"][0:8]=="/recipe/":
            newlinks.add(link["href"])
    newlinks.difference_update(bad_data)
    newlinks.difference_update(linkset)
    linkset.update(newlinks)
    for goodlink in newlinks:
        linqueue.enqueue("https://tasty.co" + goodlink)
    if i%10==0:
        print("Processed recipe #" + str(i) + " at time " + datetime.datetime.now().strftime("%X"))
        
dataList = []
index = 0
for data in dataset:
    dataList.append({"index":index, "input":data})
    index+=1

with open('who_knows.csv', encoding='utf-8', mode='w', newline='') as csvfile:
    fieldnames = dataList[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for w in dataList:
        try:
            writer.writerow(w)
        except:
            print(w)
