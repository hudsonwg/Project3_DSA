from langdetect import detect
import pandas as pd
import csv

#detect() should return "en"
print(detect('un bon bock'))
with open('english_data.csv', 'w', newline='', encoding="utf8") as csvfile:
    with open('data.csv', 'r', encoding="utf8") as data:
        reader = csv.reader(data)
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        count = 0
        for row in reader:
            try:
                if(detect(row[2].lower()) == "en"):
                    writer.writerow(row)
                    count+=1
                    print(count)
            except:
                print("translation_error")



