import matplotlib.pyplot as plt
from pymongo import MongoClient
from collections import Counter
from nltk.corpus import stopwords
import re
client = MongoClient()
hmm = client.dsbc.hmm

# challenge 1
# creating a histogram of years
cursor = hmm.find({}, {'year': 1, '_id': 0} )
years = []
for i in cursor:
    years.append(i["year"])

plt.hist(years, bins = len(set(years)))
plt.show()

# challenge 2
# finding most popular actor
cursor = hmm.find({}, {'cast': 1, '_id':0} )
cast = []
for i in cursor:
    for el in i["cast"]:
        cast.append(el)

cast_count = Counter(cast)
print cast_count.most_common(5)

# challenge 3
# find most popular non-stop word
cursor = hmm.find({}, {'title': 1, '_id':0} )
title = []
for i in cursor:
    title.append(i["title"])

lowercase_title = [w.lower() for w in title]
title_words = []
for x in lowercase_title:
    for word in x.split():
        word_a = re.sub(r'[^\w\s]', '', word)
        title_words.append(word_a)

# need to remove punctuation
filtered_word_list = title_words[:] #make a copy of the word_list
for word in title_words: # iterate over word_list
  if word in stopwords.words('english'):
    filtered_word_list.remove(word)

title_counter = Counter(filtered_word_list)
print "most common titles (minus stop words):"
print "\n"
print title_counter.most_common(5)

# challenge 4
# find most popular metal themes in the 70's, 80's, 90's
cursor = hmm.find({'year': { "$gte": 1969, "$lt": 1980}}, {'metal_cred': 1, '_id': 0})
metal_cred_1970 = []
for i in cursor:
   for theme in i['metal_cred'][1:]:
        metal_cred_1970.append(theme)

cursor = hmm.find({'year': { "$gte": 1979, "$lt": 1990}}, {'metal_cred': 1, '_id': 0})
metal_cred_1980 = []
for i in cursor:
   for theme in i['metal_cred'][1:]:
        metal_cred_1980.append(theme)

cursor = hmm.find({'year': { "$gte": 1989, "$lt": 2000}}, {'metal_cred': 1, '_id': 0})
metal_cred_1990 = []
for i in cursor:
    for theme in i['metal_cred'][1:]:
        metal_cred_1990.append(theme)

print "\n"

# printing out the most common themes by decade
seventies_count = Counter(metal_cred_1970)
print "1970 most common: "
print seventies_count.most_common(3)
eighties_count = Counter(metal_cred_1980)
print "1980 most common: "
print eighties_count.most_common(3)
nineties_count = Counter(metal_cred_1990)
print "1990 most common: "
print nineties_count.most_common(3)
