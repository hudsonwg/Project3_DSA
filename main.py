import math
import random
from langdetect import detect
import csv

def getAllSimilarities(m1, m2):
    #get similarities between two pieces of media and return them as an array
    intersection = (set(m1.genres).intersection(m2.genres))
    ra = []
    for i in intersection:
        ra.append(i)
    try:
        if (m1.decade == m2.decade):
            ra.append(m1.decade)
        if (m1.media_type == m2.media_type):
            ra.append(m1.media_type)
        if (m1.runtime == m2.runtime):
            ra.append(m1.runtime)
    except:
        toggle = False
    return ra
def processData():
    # detect() should return "en"
    with open('english_data.csv', 'w', newline='', encoding="utf8") as csvfile:
        with open('data.csv', 'r', encoding="utf8") as data:
            reader = csv.reader(data)
            writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            count = 0
            for row in reader:
                try:
                    if (detect(row[2].lower()) == "en"):
                        writer.writerow(row)
                        count += 1
                        print(count)
                except:
                    print("translation_error")

class Media:
    def __init__(self, title, decade, media_type, runtime, genres):
        self.title = title
        self.decade = decade
        self.media_type = media_type
        self.runtime = runtime
        self.genres = genres
        self.similar = []
        self.sorted = False

def getSimilarity(m1, m2):
    # returns similarity between two media sources, based off of all their attributes
    decadeWeight = 0.3
    typeWeight = 0.1
    runtimeWeight = 0.1
    genresWeight = 0.5

    similarity = 0

    # (total of both lengths of array - union*2)
    length = len(m1.genres) + len(m2.genres)
    intersection = len(set(m1.genres).intersection(m2.genres)) * 2
    genreSimilarity = intersection / length
    similarity += genresWeight * genreSimilarity
    try:
        if (m1.decade == m2.decade):
            similarity += decadeWeight
        elif (math.abs(int(m1.decade[2:4]) - int(m2.decade[2:4])) <= 10):
            similarity += decadeWeight * 0.6
        if (m1.media_type == m2.media_type):
            similarity += typeWeight
        if (m1.runtime == m2.runtime):
            similarity += runtimeWeight
    except:
        print("at least one attribute could not be compared")
    return round(similarity, 4)

def printMedia(media):
    print(media.title)
    print(media.decade)
    print(media.media_type)
    print(media.runtime)
    print(media.genres)

def approach1():
    mediaContainer = []
    with open('english_data.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # READ THE DATA FROM ROW AND INSERT INTO A CLASS OBJECT, THEN INSERT THAT OBJECT INTO THE DATA STRUCTURE
            try:
                time = int(row[7])
            except:
                runtime = "unknown"
            runtime = ""
            if (time < 5):
                runtime = "less than 5 minutes"
            elif (time < 60):
                runtime = "less than 1 hour"
            elif (time < 120):
                runtime = "less than 2 hours"
            elif (time > 120):
                runtime = "longer than 2 hours"

            genres = row[8].split(",")

            media_to_insert = Media(row[2].replace(",", " "), row[5][0:2] + "00's", row[1], runtime, genres)
            mediaContainer.append(media_to_insert)
        # HASHMAP  NAME: OBJECT
        # SORTED ARRAY, insert first object no need to sort

        # EVERY OTHER OBJECT, GO TO RANDOM OBJECT IN SORTED LISTS LOCATION, AND RUN SIMILARITY CHECK ON ALL IT's ADJACENT NEIGHBORS
        # then go to neighbor with highest similarity and do the same thing
        # do this, until you revisit the previous node, make sure similarity score meets a certain threshold to neighbors

        nameMap = {}
        sorted = []

        nameMap[mediaContainer[0].title] = mediaContainer[0]
        sorted.append(mediaContainer[0])

        for i in range(1, len(mediaContainer)):
            print(i)
            index = random.randint(0, len(sorted) - 1)
            currentNode = sorted[index]
            if (len(currentNode.similar) == 0):
                currentNode.similar.append(mediaContainer[i].title)
                mediaContainer[i].similar.append(currentNode.title)
                nameMap[mediaContainer[i].title] = mediaContainer[i]
                sorted.append(mediaContainer[i])
            else:
                found = False
                while (found == False):
                    max = getSimilarity(currentNode, mediaContainer[i])
                    name = currentNode.title
                    for m in currentNode.similar:
                        if getSimilarity(nameMap[m], mediaContainer[i]) > max:
                            name = nameMap[m].title
                            max = getSimilarity(nameMap[m], mediaContainer[i]) > max
                    if (name == currentNode.title):
                        # insert node and break
                        if (len(currentNode.similar) == 1):
                            currentNode.similar.append(mediaContainer[i].title)
                            mediaContainer[i].similar.append(currentNode.title)
                            sorted.append(mediaContainer[i])
                            nameMap[mediaContainer[i].title] = mediaContainer[i]
                            found = True
                        else:
                            mediaContainer[i].similar.append(currentNode.title)
                            mediaContainer[i].similar.append(currentNode.similar[0])
                            currentNode.similar = [mediaContainer[i].title, currentNode.similar[1]]
                            nameMap[mediaContainer[i].title] = mediaContainer[i]
                            sorted.append(mediaContainer[i])
                            found = True
                    else:
                        currentNode = nameMap[name]



    print("writing to file")
    with open('sorted_output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        for m in sorted:
            i1 = []
            i1.append(m.similar[0])
            i1.append(str(getAllSimilarities(nameMap[m.similar[0]], m)).replace(",", " ").replace("[", "").replace("]", ""))
            if(len(m.similar)==2):
                i1.append(m.similar[1])
                i1.append(str(getAllSimilarities(nameMap[m.similar[1]], m)).replace(",", " ").replace("[", "").replace("]", ""))
            #try:
                #i1.append(nameMap[m.similar[0]].similar[0])
                #i1.append(str(getAllSimilarities(nameMap[nameMap[m.similar[0]].similar[0]], m)).replace(",", " ").replace("[", "").replace("]", ""))
                #i1.append(nameMap[m.similar[1]].similar[1])
                #i1.append(str(getAllSimilarities(nameMap[nameMap[m.similar[1]].similar[0]], m)).replace(",", " ").replace("[", "").replace("]", ""))
            #except:
                #print("add this functionality later")
            output = m.title
            output+=","
            output+=str(m.genres).replace(",", " ").replace("[", "").replace("]", "")
            output+=" "+m.decade
            output+=" "+m.media_type
            output+=" "+m.runtime
            for i in i1:
                output+=","
                output+=i

            writer.writerow([output])

    return mediaContainer

def run_program():
    running = True
    while running == True:
        response = input("Search A Movie: ")
        with open('sorted_output.csv', 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            found = False
            for row in reader:
                if(row[0] == response):
                    found = True
                    print(row)
                    break
            if(found == False):
                print("COULD NOT FIND MOVIE")


if __name__ == '__main__':
    #processData()
    #approach1()
    run_program()

