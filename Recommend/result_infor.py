from bs4 import BeautifulSoup
import urllib2
import csv
import json
# from BeautifulSoup import BeautifulSoup
#import pymssql
import pandas as pd

import requests
import timeit

import time




csv.register_dialect(
    'mydialect',
    delimiter = '\t',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\r\n',
    quoting = csv.QUOTE_MINIMAL)
    
def get_personal_data(people):
    result=[]
    for person in people:
        result.append(person['name']['nconst'])
    return ','.join(result)
def get_film_director_creator(creator_data, director_data):
    result = []
    result.append(get_personal_data(creator_data))
    result.append(get_personal_data(director_data))
    
    return ','.join(filter(None, result))
    
    
df = pd.read_csv('/home/honglanh/Documents/Result/Result_step_data/match_one_result.csv',sep='\t', names=['ID', 'tag'])
with open('/home/honglanh/Documents/Result/result_movies1.csv', 'w') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile, dialect='mydialect')   
    csv_header = ['IDPayTV', 'IDIMDB', 'Title', 'Rating', 'VoteNum', 'Year', 'Type', 'Genres', 'ReleaseDate',
                  'Duration', 'IDStars', 'IDDirectors', 'Country', 'Language', 'Description']
    thedatawriter.writerow(csv_header)
        
    for index, row in df.iterrows():
        start = timeit.default_timer()
        s = row['tag'].split('/')
        url1 = 'http://app.imdb.com/title/maindetails?tconst=' + s[2]
        
        resp = requests.get(url1).json()
        data = resp['data']
        
        fpt_play_id = row['ID']
        
        imdb_id = s[2]
##     
        title = data['title'].encode('utf-8') + '(' + data['year'].encode('utf-8') +')'
##       
        film_rating = ''
        if ('rating' in data):
            film_rating = data['rating']
##
        film_votes = ''
        if ('num_votes' in data):
            film_votes = data['num_votes']
##        
        film_year = data['year']
##       
        film_type = data['type']
##           
        genres = ''
        if ('genres' in data):
            genres = ",".join(data['genres'])
##        
        release_date = ''
        if ('release_date') in data:
            release_date = data['release_date']['normal']
##       
        film_duration = ''
        if ('runtime' in data and 'time' in data['runtime']):
            film_duration = data['runtime']['time']
            #film_duration = time.strftime('%Hh %Mmin', time.gmtime(film_duration))
##            
        film_stars = ''
        if ('cast_summary' in data):
            film_stars = get_personal_data(data['cast_summary'])      
        
##       
        creator_data = []
        director_data = []
        if ('creators' in data):
            creator_data = data['creators']
        if ('directors_summary' in data):
            director_data = data['directors_summary']
            
        film_director_creator = ''
        if (len(director_data) > 0 or len(creator_data) > 0):
            film_director_creator = get_film_director_creator(creator_data, director_data)
##           
        url2 = 'http://www.omdbapi.com/?i=' + s[2]
        
        data2 = requests.get(url2).json()
##      
        film_country = ''
        if ('Country' in data2):
            film_country = data2['Country']
##
        if ('Language' in data2):
            film_language = data2['Language']
                    
##       
        film_desc = ''
        if ('Plot' in data2):
            film_desc = data2['Plot'].encode('utf-8')
        #if (('best_plot' in data) and ('outline' in data['best_plot'])):
            #film_desc = data['best_plot']['outline']
            #film_desc = film_desc.encode('utf-8')
        
        row_data = [fpt_play_id, imdb_id, title, film_rating, film_votes, film_year,
                    film_type, genres,release_date, film_duration, film_stars, film_director_creator,film_country, film_language, film_desc]
        thedatawriter.writerow(row_data)
        
        stop = timeit.default_timer()
        print s[2], stop - start
        
print('\n\nDone.Finished')
  
    


