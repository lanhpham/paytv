
import pandas as pd
import glob

# now, load it into pandas
out_path = "/Users/sondinh/Downloads/python/bf_only_vectordays/output/"
input_path = '/Users/sondinh/Downloads/python/bf_only_vectordays/json/'
allFiles = glob.glob(path + "/*.txt")
data_status_2 = []
data_status_3 = []
header =  ['Contract', 'CustomerId', 'Status']
for my_file in allFiles:
    pd.read_json(my_file)
    test = data_df.ix[1,0]
    temp = []
    for i in test:
        if (i['Status']=='3'):
            data_status_3.append(i)
        if (i['Status']=='2'):
            data_status_2.append(i)
    
            
score1 = pd.DataFrame(data = data_status_3)
score1.to_csv(out_path +str(1).zfill(3) + "thread.txt", header = header, index = False)
score2 = pd.DataFrame(data = data_status_2)
score2.to_csv(out_path +str(2).zfill(3) + "thread.txt", header = header, index = False)
