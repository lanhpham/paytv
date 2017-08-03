import pandas as pd
from sklearn.cluster import KMeans

#%%
df_t3 = pd.read_csv(DIR + 't3.csv', sep = ',')
#%%
t3_hourly = pd.read_csv(DIR + 't3/vectorHourly.csv')
t3_hourly = t3_hourly.replace("null", "0", regex=True)
t3_hourly.ix[:,1:25] = t3_hourly[t3_hourly.columns.values[1:25]].astype(int)
t3_hourly = pd.merge(t3_hourly, df_t3[["CustomerId","Churn"]], on = "CustomerId", how = "inner")

#%%
kmeans = KMeans(n_clusters = 4)
kmeans.fit(t3_hourly.ix[:,1:25])
t3_result = pd.DataFrame(data=kmeans.labels_, columns = ["cluster"], index = t3_hourly["CustomerId"])
t3_result = df_t3.join(t3_result, how = "inner", on = "CustomerId")
#%%
print t3_result["cluster"].value_counts()
print t3_result[t3_result["Churn"] == True]["cluster"].value_counts()
#%%
for i in range(4):
    t3_result[t3_result["cluster"] == i].to_csv(DIR + "test_" + str(i) + ".csv", index = False)    
#%%
churn = df_t3.ix[:,-1]
feature1 = df_t3.ix[:,1]
feature2 = df_t3.ix[:,2]
feature3 = df_t3.ix[:,3]
#%%
import matplotlib.pyplot as plt
plt.hist(churn)
#%%
plt.hist([feature1, feature2, feature3])
#%%
import seaborn as sns
g = sns.pairplot(churn)
#%%
feature1.describe()
feature2.describe()
feature3.describe()
#%%
import seaborn as sns

data = pd.melt(df_t3, id_vars=['CustomerId', 'Churn'], value_vars=['Time1', 'Time2', 'Time3'], var_name='Time', value_name='Duration')
#%%
sns.barplot(x='Time', y='Duration', hue='Churn', data=data)
#%%
sns.countplot(x = 'Time', hue= 'Churn', data = data)

#%%
sns.boxplot(x='Time', y='Duration', hue='Churn', data=data, fliersize=0)