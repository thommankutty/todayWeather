# import modules here
import requests
from bs4 import BeautifulSoup as BS
import sqlite3
import time
# import link here
link = r'http://www.weather.gov.sg/home'

# request on the link
page = requests.get(link).content

# apply bs4
content = BS(page, 'lxml')

name_box = content.find_all('div', attrs={'class': 'media-body media-middle'}) # returns <div class="media-body media-middle"> <h2>33°C</h2> </div>

# find temp high
temp_high = name_box[0].find('h2').text

# find temp high
temp_low = name_box[1].find('h2').text

# find description
description =  content.find_all('div', attrs={'class': 'col-xs-5 title title-spacer'})[0].find('p').text

date =  (time.strftime("%d/%m/%Y"))

conn = sqlite3.connect("weatherDataBase.db")  # or use :memory: to put it in RAM

cursor = conn.cursor()

# cursor.execute("""DROP TABLE weatherData""")
#
# conn.commit()
# conn.close()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS weatherData (date text PRIMARY KEY, temp_high TEXT,
                       temp_low TEXT, description TEXT)
''')

cursor.execute('''INSERT INTO weatherData(date, temp_high, temp_low, description)
                  VALUES(?,?,?,?)''', (date,temp_high,temp_low,description))

print('today is     :' + date)
print('temp_high is :'+temp_high)
print('temp_low is  :'+temp_low)
print(description)


conn.commit()
conn.close()

# input()