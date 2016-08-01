from bs4 import BeautifulSoup
import urllib2
import requests
import pandas as pd
import timeit
import csv

csv.register_dialect(
    'mydialect',
    delimiter = '\t',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\n',
    quoting = csv.QUOTE_MINIMAL)
    

df = pd.read_csv('/home/honglanh/Documents/Result/result_id.csv',header = 0, 
                 names=['IDPerson']) 
                 
with open ('/home/honglanh/Documents/Result/Result_name.csv', 'w') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile, dialect='mydialect')   
    csv_header = ['IDPerson', 'Name', 'Real_Name']
    thedatawriter.writerow(csv_header)
   
    for index, row in df.iterrows():
        start = timeit.default_timer()
        
        url = 'http://app.imdb.com/name/maindetails?nconst=' + row['IDPerson']
        
        resp = requests.get(url).json()
        
        data = resp['data']
        
        name_person = ''
        real_name_person = ''
        if 'name' in data:
            name_person = data['name'].encode('utf-8')
        if 'real_name' in data:
            real_name_person = data['real_name'].encode('utf-8')
            
        id_person = row['IDPerson']
        
        raw_data = [id_person,name_person, real_name_person]
        thedatawriter.writerow(raw_data)
        
        stop = timeit.default_timer()
        
        print stop - start
        
print '\n Finished'
    