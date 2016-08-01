from bs4 import BeautifulSoup
import urllib2
import requests
import pandas as pd
import time
import csv
csv.register_dialect(
    'mydialect',
    delimiter = '\t',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\n',
    quoting = csv.QUOTE_MINIMAL)


df = pd.read_csv('/home/honglanh/Downloads/no_rating_match_one_result.csv',
                 sep = '\t', names = ['ID', 'tag'])
              
with open('/home/honglanh/Documents/Result/result_id3.csv', 'w') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile, dialect='mydialect')   
    csv_header = ['IDPerson']
    thedatawriter.writerow(csv_header)
    id_person = []
    
    for index, row in df.iterrows():
        start = timeit.default_timer()
        s = row['tag'].split('/')
        url = 'http://app.imdb.com/title/maindetails?tconst=' + s[2]
        resp = requests.get(url).json()
        data = resp['data']
        
        creator_data = ''
        director_data = ''
        if ('creators' in data):
            creator_data = data['creators']
            
        if ('directors_summary' in data):
            director_data = data['directors_summary']
            
        
        if (len(director_data) > 0):
            for i in director_data:
                id_person.append(i['name']['nconst'])
                
            
        if  (len(creator_data) > 0):
            for i in creator_data:
                id_person.append(i['name']['nconst'])
                
        
        star_data = ''
        if ('cast_summary' in data):
            star_data = data['cast_summary']
            for i in star_data:
                id_person.append(i['name']['nconst'])
        
        
    distinct_id_person = list(set(id_person))
    sorted_id = sorted(distinct_id_person)
    for id_item in sorted_id:
        raw_data = [id_item]
        thedatawriter.writerow(raw_data)
    
        stop = timeit.default_timer()
        print stop - start
    
print '\n Finished'
        
        
    
          
