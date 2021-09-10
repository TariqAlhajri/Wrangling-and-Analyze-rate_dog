#!/usr/bin/env python
# coding: utf-8

# # Project: Wrangling and Analyze Data

# In[1]:


import pandas as pd
import numpy as np
import requests 
import matplotlib.pyplot as plt 
import seaborn as sb


# ## Data Gathering
# In the cell below, gather **all** three pieces of data for this project and load them in the notebook. **Note:** the methods required to gather each data are different.
# 1. Directly download the WeRateDogs Twitter archive data (twitter_archive_enhanced.csv)

# In[2]:


#Download twitter-archive-enhanced using read_csv pandas's method
twitter_archive = pd.read_csv('twitter-archive-enhanced.csv')
#View the first couple of rows
twitter_archive.head()


# 2. Use the Requests library to download the tweet image prediction (image_predictions.tsv)

# In[3]:


#first save the url link
url = "https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv"
response = requests.get(url)
with open('image_predictions.tsv', 'wb') as file:
    file.write(response.content)
image_predictions = pd.read_csv('image_predictions.tsv', sep='\t')
#View the first couple of lines in image_predictions data
image_predictions.head()


# 3. Use the Tweepy library to query additional data via the Twitter API (tweet_json.txt)

# In[4]:


#Reading the json file by using read_json pandas's method
tweet_json = pd.read_json('tweet-json.txt',lines=True)
#View the first 4 rows
tweet_json.head(4)


# ## Assessing Data
# In this section, detect and document at least **eight (8) quality issues and two (2) tidiness issue**. You must use **both** visual assessment
# programmatic assessement to assess the data.
# 
# **Note:** pay attention to the following key points when you access the data.
# 
# * You only want original ratings (no retweets) that have images. Though there are 5000+ tweets in the dataset, not all are dog ratings and some are retweets.
# * Assessing and cleaning the entire dataset completely would require a lot of time, and is not necessary to practice and demonstrate your skills in data wrangling. Therefore, the requirements of this project are only to assess and clean at least 8 quality issues and at least 2 tidiness issues in this dataset.
# * The fact that the rating numerators are greater than the denominators does not need to be cleaned. This [unique rating system](http://knowyourmeme.com/memes/theyre-good-dogs-brent) is a big part of the popularity of WeRateDogs.
# * You do not need to gather the tweets beyond August 1st, 2017. You can, but note that you won't be able to gather the image predictions for these tweets since you don't have access to the algorithm used.
# 
# 

# ### Quality issues
# 1.**twitter_archive:** timestamp as object (string), needs to be converted to DateTime datatype.
# 
# 2.**twitter_archive:** tweet_id as int64, needs to be converted to String datatype.
# 
# 3.**twitter_archive:** deals with records that has a denomiator higher than 10.
# 
# 4.**twitter_archive:** data in source column has a href html tag, needs to be fixed.
# 
# 5.**twitter_archive:** delete all retweeted tweets 'duplicate tweets'.

# ### Tidiness issues
# 1.**twitter_archive:** doggo, floofer, pupper and puppo needs to be in one column rather than 4."Each variable is a column"
# 
# 2.**twitter_archive:** remove unnecessary columns(in_reply_to_status_id, in_reply_to_user_id, retweeted_status_id, retweeted_status_user_id, retweeted_status_timestamp)

# ## Assesing || twitter_archive dataset

# In[5]:


#check the datatype of twitter archive df
twitter_archive.info()


# In[6]:


#View all record that has a denomiator higher than 10 which not right according to the documentation of the dataset
twitter_archive.rating_denominator.value_counts()
#As we can see the is a couple of records that has a denomiator higher, will try to
#fix it or delete it if neccassery


# In[7]:


#query tweets with denominator higher that 10.
high_deno= twitter_archive.query('rating_denominator >10')
high_deno


# In[8]:


tweet_id= high_deno['tweet_id']
text= high_deno['text']

for point in zip(tweet_id, text):
    print("tweet Id:{} \n text: {} \n ----------------".format(*point))


# - **Tweet Id**  832088576586297345: This tweet needs to be deleted, no rating provided.
# - **Tweet Id**  820690176645140481: Wrong rating provided, needs to be deleted.
# - **Tweet Id**  775096608509886464: I've noticed that this a retweeted tweet for tweet with index **740373189193256964**, need to delete all retweeted tweets since its a duplicate ones.
# - **Tweet Id**  758467244762497024: Wrong rating provided, needs to be deleted.
# - **Tweet Id** 740373189193256964: Wrong captured data from tweet, actual rating is 14/10.
# - **Tweet Id** 731156023742988288: Wrong rating provided, needs to be deleted.
# - **Tweet Id** 722974582966214656: Wrong data captured, actual rating is 13/10.
# - **Tweet Id** 716439118184652801: Wrong data captured, actual rating is 11/10.
# - **Tweet Id** 713900603437621249: Wrong rating provided, needs to be deleted.
# - **Tweet Id** 710658690886586372: rating can be change to 10/10 since it same as 80/80.
# - **Tweet Id** 709198395643068416: Wrong rating provided, needs to be deleted.
# - **Tweet Id** 704054845121142784: Wrong rating provided, needs to be deleted.
# - **Tweet Id** 697463031882764288: Wrong rating provided, needs to be deleted.
# - **Tweet Id** 686035780142297088: Wrong rating provided, needs to be deleted.
# - **Tweet Id** 684225744407494656: Wrong rating provided, needs to be deleted.
# - **Tweet Id** 684222868335505415: Wrong rating provided, needs to be deleted.
# - **Tweet Id** 682962037429899265:tweet isn't clear for me, I guess the acutal rating is 10/10 not 7/11
# - **Tweet Id** 682808988178739200:Wrong rating provided, needs to be deleted.
# - **Tweet Id** 677716515794329600:Wrong rating provided, needs to be deleted.
# - **Tweet Id** 675853064436391936:Wrong rating provided, needs to be deleted.
# 

# In[9]:


#Checkif there is any duplicated values
twitter_archive.duplicated().sum()


# ----------
# ## Assesing2 || image_predictions dataset

# ### Quality issues
# 1.**image_predictions:** Remove duplicate jpg_url.
# 
# 2.**image_predicitons:** Change datatype of tweet_id column

# ### Tidness issues
# 1.**image_prediction:** extract the breed of dog from the p,p_conf and p_dog columns.

# In[10]:


#check datatypes of columns
image_predictions.info()


# In[11]:


#check for duplicate reocrds.
image_predictions.duplicated().sum()


# In[12]:


#check for duplicate jpg_url since the prediction is based on it.
image_predictions['jpg_url'].duplicated().sum()
#there is 66 duplicate photo that has to be deleted.


# In[13]:


image_predictions.describe()


# ------------------------
# ## Assesing3 || tweet_json dataset

# ### Quality issues
# 1.**tweet_json:** rename "id" column to tweet_id and change datatype to String.
# 
# 2.**tweet_json:** remove href tag from source column.

# ### Tidness issues
# 1.**tweet_json:** We only need favorite_count, retweet count,id "tweet_id" (after renamed), and source columns.

# In[14]:


tweet_json.head(5)


# In[15]:


tweet_json.info()


# In[16]:


#check for duplicate tweets.
tweet_json['id'].duplicated().sum()
#no duplicate id.


# In[17]:


#see the count for all unique values for source column.
tweet_json['source'].value_counts()


# ## Cleaning Data
# In this section, clean **all** of the issues you documented while assessing. 
# 
# **Note:** Make a copy of the original data before cleaning. Cleaning includes merging individual pieces of data according to the rules of [tidy data](https://cran.r-project.org/web/packages/tidyr/vignettes/tidy-data.html). The result should be a high-quality and tidy master pandas DataFrame (or DataFrames, if appropriate).

# ### Quality issues
# 1.**twitter_archive:** timestamp as object (string), needs to be converted to DateTime datatype.
# 
# 2.**twitter_archive:** tweet_id as int64, needs to be converted to String datatype.
# 
# 3.**twitter_archive:** delete all retweeted tweets 'duplicate tweets'.
# 
# 4.**twitter_archive:** data in source column has a href html tag, needs to fixed.
# 
# 5.**twitter_archive:** deals with records that has a denominator higher than 10.
# 
# 6.**image_predictions:** Remove duplicates jpg_url.
# 
# 7.**image_predicitons:** Change datatype of tweet_id column to String.
# 
# 8.**tweet_json:** rename "id" column to tweet_id and change datatype to String.
# 

# ### Tidness issues
# 9.**twitter_archive:** doggo, floofer, pupper and puppo needs to be in one column rather than 4."Each variable is a column"
# 
# 10.**twitter_archive:** remove unnecessary columns(in_reply_to_status_id, in_reply_to_user_id, retweeted_status_id, retweeted_status_user_id, retweeted_status_timestamp)
# 
# 11.**image_prediction:** extract the breed of dog from the p,p_conf and p_dog columns.
# 
# 12.**tweet_json:** We only need favorite_count, retweet count,id "tweet_id" (after renamed), and source columns.

# In[18]:


# Make copies of original pieces of data
twitter_archive_clean= twitter_archive.copy()
tweet_json_clean= tweet_json.copy()
image_predictions_clean= image_predictions.copy()


# ------------------------
# ## Cleaning1 || twitter_archive dataset

# 1.**twitter_archive:** timestamp as object (string), needs to be converted to DateTime datatype.
# 
# 2.**twitter_archive:** tweet_id as int64, needs to be converted to String datatype.
# 
# 3.**twitter_archive:** delete all retweeted tweets 'duplicate tweets'.
# 
# 4.**twitter_archive:** data in source column has a href html tag, needs to fixed.
# 
# 5.**twitter_archive:** deals with records that has a denominator higher than 10.
# 
# 6.**twitter_archive:** doggo, floofer, pupper and puppo needs to be in one column rather than 4."Each variable is a column"
# 
# 7.**twitter_archive:** remove unnecessary columns(in_reply_to_status_id, in_reply_to_user_id, retweeted_status_id, retweeted_status_user_id, retweeted_status_timestamp).

# 
# ### Issue #1: 
# timestamp as object (string), needs to be converted to DateTime datatype.

# #### Define: 
# change timestamp datatype from String to datetime by method to_dateTime()

# #### Code

# In[19]:


#converting datatype to datetime
twitter_archive_clean['timestamp'] = pd.to_datetime(twitter_archive_clean['timestamp'])


# #### Test

# In[20]:


#check datatypes
twitter_archive_clean.dtypes


# ### Issue #2:
# tweet_id as int64, needs to be converted to String datatype.
# 

# #### Define 
# convert tweet_id from int to String by method astype

# #### Code

# In[21]:


#change the datatype to String by using method astype to column 'tweet_id'
twitter_archive_clean['tweet_id']= twitter_archive_clean['tweet_id'].astype(str)


# #### Test

# In[22]:


twitter_archive_clean.dtypes


# ### Issue #3:
# delete all retweeted tweets 'duplicate tweets'.
# 
# 

# #### Define 
# delete retweeted tweets.

# #### Code

# In[23]:


#cleaning the retweeted tweets by selecting rows that have null in reteeted_status_user_id column
twitter_archive_clean = twitter_archive_clean[pd.isnull(twitter_archive_clean['retweeted_status_user_id'])]


# #### Test

# In[24]:


#all nan values
twitter_archive_clean['retweeted_status_user_id'].unique()
#there is only nan value in retweeted ststus user id


# ### Issue #4:
# data in source column has a href html tag, needs to fixed.

# #### Define 
# source is in form of href, needs to be changed to twitter for iPhone, vine, twitter for Web

# #### Code

# In[25]:


#first check all unique values.
twitter_archive_clean.source.value_counts()


# In[26]:


#by using the method loc to change the value of certain column if a condition is met.
twitter_archive_clean.loc[twitter_archive_clean['source'].str.contains('iPhone') , 'source'] = 'Twitter for iPhone'
twitter_archive_clean.loc[twitter_archive_clean['source'].str.contains('Vine') , 'source'] = 'Vine'
twitter_archive_clean.loc[twitter_archive_clean['source'].str.contains('Web') , 'source'] = 'Twitter for Web'
twitter_archive_clean.loc[twitter_archive_clean['source'].str.contains('TweetDeck') , 'source'] = 'TweetDeck'


# #### Test

# In[27]:


#Now check again to see if it works.
twitter_archive_clean.source.value_counts()


# ### Issue #5:
# deals with records that has a denomiator higher than 10.

# - **Tweet Id**  832088576586297345: This tweet needs to be deleted, no rating provided.
# - **Tweet Id**  820690176645140481: Wrong rating provided, needs to be deleted.
# - **Tweet Id**  775096608509886464: I've noticed that this a retweeted tweet for tweet with Id **740373189193256964**, need to delete all retweeted tweets since its a duplicate ones.
# - **Tweet Id**  758467244762497024: Wrong rating provided, needs to be deleted.
# - **Tweet Id** 740373189193256964: Wrong captured data from tweet, actual rating is 14/10.
# - **Tweet Id** 731156023742988288: Wrong rating provided, needs to be deleted.
# - **Tweet Id** 722974582966214656: Wrong data captured, actual rating is 13/10.
# - **Tweet Id** 716439118184652801: Wrong data captured, actual rating is 11/10.
# - **Tweet Id** 713900603437621249: Wrong rating provided, needs to be deleted.
# - **Tweet Id** 710658690886586372: rating can be change to 10/10 since it same as 80/80.
# - **Tweet Id** 709198395643068416: Wrong rating provided, needs to be deleted.
# - **Tweet Id** 704054845121142784: Wrong rating provided, needs to be deleted.
# - **Tweet Id** 697463031882764288: Wrong rating provided, needs to be deleted.
# - **Tweet Id** 686035780142297088: Wrong rating provided, needs to be deleted.
# - **Tweet Id** 684225744407494656: Wrong rating provided, needs to be deleted.
# - **Tweet Id** 684222868335505415: Wrong rating provided, needs to be deleted.
# - **Tweet Id** 682962037429899265:tweet isn't clear for me, I guess the acutal rating is 10/10 not 7/11
# - **Tweet Id** 682808988178739200:Wrong rating provided, needs to be deleted.
# - **Tweet Id** 677716515794329600:Wrong rating provided, needs to be deleted.
# - **Tweet Id** 675853064436391936:Wrong rating provided, needs to be deleted.
# 

# #### Define 
# delete all records that has wrong rating and fixed recrods that have captured wrong data from tweets.

# #### Code

# In[28]:


#fixing the remaining row manually: -
#first delete the rows with wrong ratings
id_list=[832088576586297345, 820690176645140481, 758467244762497024, 731156023742988288, 713900603437621249, 
         709198395643068416, 704054845121142784, 697463031882764288, 686035780142297088, 684225744407494656, 
         684222868335505415, 682808988178739200, 677716515794329600, 675853064436391936]
for i in id_list:
    twitter_archive_clean=twitter_archive_clean.query('tweet_id !="{}"'.format(i))
    
#Now fix recrods that caputred wrong data: -
twitter_archive_clean.loc[twitter_archive_clean['tweet_id'] =='740373189193256964', 'rating_numerator'] = 14
twitter_archive_clean.loc[twitter_archive_clean['tweet_id'] =='740373189193256964', 'rating_denominator'] = 10

twitter_archive_clean.loc[twitter_archive_clean['tweet_id'] =='722974582966214656', 'rating_numerator'] = 13
twitter_archive_clean.loc[twitter_archive_clean['tweet_id'] =='722974582966214656', 'rating_denominator'] = 10

twitter_archive_clean.loc[twitter_archive_clean['tweet_id'] =='716439118184652801', 'rating_numerator'] = 11
twitter_archive_clean.loc[twitter_archive_clean['tweet_id'] =='716439118184652801', 'rating_denominator'] = 10

twitter_archive_clean.loc[twitter_archive_clean['tweet_id'] =='710658690886586372', 'rating_numerator'] = 10
twitter_archive_clean.loc[twitter_archive_clean['tweet_id'] =='710658690886586372', 'rating_denominator'] = 10

twitter_archive_clean.loc[twitter_archive_clean['tweet_id'] =='682962037429899265', 'rating_numerator'] = 10
twitter_archive_clean.loc[twitter_archive_clean['tweet_id'] =='682962037429899265', 'rating_denominator'] = 10


# #### Test

# In[29]:


len(twitter_archive_clean.query('rating_denominator > 10'))
#there is 0 records 


# ### Issue #6:
#  doggo, floofer, pupper and puppo needs to be in one column rather than 4."Each variable is a column"
# 

# #### Define 
# these columns represents the stage of dogs, needs to have one column named "dog_stage".

# #### Code

# In[30]:


#create a method that set the value of column 'dog_stage' based on the velue of doggo, floofer, pupper, and puppo columns
def stage(row):
    #if doggo has the value 'doggo', dog_stage column for this row is 'doggo'
    if row['doggo'] == 'doggo':
        val = 'doggo'
    #if floofer has the value 'doggo', dog_stage column for this row is 'floofer'
    elif row['floofer'] == 'floofer':
        val = 'floofer'
    #if pupper has the value 'doggo', dog_stage column for this row is 'pupper'
    elif row['pupper'] == 'pupper':
        val = 'pupper'
    #if pippo has the value 'doggo', dog_stage column for this row is 'puppo'
    elif row['puppo']=='puppo':
        val = 'puppo'
    #if all none, then the value for it is None
    else:
        val = None
    return val
twitter_archive_clean['dog_stage'] = twitter_archive_clean.apply(stage, axis=1)


# #### Test

# In[31]:


#check if method is successfully done and see if there is a recond that has none in pupper column and pupper in dog_stage
twitter_archive_clean.query('dog_stage == pupper and pupper == None')

#Now delete the doggo, floofer, pupper and puppo columns
twitter_archive_clean= twitter_archive_clean.drop(['doggo', 'floofer', 'pupper', 'puppo'], axis=1)


# ### Issue #7:
# Remove unnecessary columns(in_reply_to_status_id, in_reply_to_user_id, retweeted_status_id, retweeted_status_user_id, retweeted_status_timestamp)

# #### Define 
# drop unnecessary columns in twitter archive dataset

# #### Code

# In[32]:


twitter_archive_clean= twitter_archive_clean.drop(['in_reply_to_status_id', 'in_reply_to_user_id', 
                                                   'retweeted_status_id', 'retweeted_status_user_id', 
                                                   'retweeted_status_timestamp','expanded_urls' ], axis=1)


# #### Test

# In[33]:


twitter_archive_clean.info()


# ------------------------
# ## Cleaning 2 ||  image_predictions dataset

# 1.**image_predictions:** Remove duplicate jpg_url.
# 
# 2.**image_predicitons:** Change datatype of tweet_id column to String.
# 
# 3.**image_prediction:** extract the breed of dog from the p,p_conf and p_dog columns.

# ### Issue #8:
# Remove duplicate jpg_url.

# #### Define 
# remove records that has a duplicate value jpg_url.

# #### Code

# In[34]:


image_predictions_clean= image_predictions_clean.drop_duplicates(subset='jpg_url', keep="first")
image_predictions_clean.head(3)


# #### Test

# In[35]:


#check for duplicate in column jpg_url
image_predictions_clean.jpg_url.duplicated().sum()


# ### Issue #9:
# Change datatype of tweet_id column to String.

# #### Define 
# Change datatype of tweet_id column to Stirng by method astype()

# #### Code

# In[36]:


image_predictions_clean['tweet_id']= image_predictions_clean['tweet_id'].astype(str)


# #### Test

# In[37]:


image_predictions_clean.dtypes


# ### Issue #10:
#  extract the breed of dog from the p,p_conf and p_dog columns.

# #### Define 
# extract the breed of dog using a function detect_breed and creating a new column called breed_of_dog

# In[38]:


image_predictions_clean.head(4)


# #### Code

# In[39]:


#I'm only seeing if Pn_dog since the predictions is arranged from the strongest by (pn_conf), so checking if p1_dog is True without
#checking the Pn_dog is enough.
def extract_breed (row):
    breed=''
    if row['p1_dog']==True :
        breed=row['p1']
    elif row['p2_dog']==True : 
         breed=row['p2']
    elif row['p3_dog']==True :
        breed=row['p3']
    else:
        breed= None

    return breed
#now I'm calling the function to create the new column: -
image_predictions_clean['breed_of_dog']= image_predictions_clean.apply (lambda row: extract_breed(row), axis=1) 
#drop the the p1,p1_dog,p2_conf....etc 

image_predictions_clean= image_predictions_clean.drop(['p1', 'p1_conf','p1_dog','p2','p2_conf',
                                                       'p2_dog','p3','p3_conf','p3_dog','img_num'], axis=1)


# #### Test

# In[40]:


image_predictions_clean.head(4)


# ---------------------
# ### Cleaning 3 || tweet_json dataset

# 1.**tweet_json:** rename "id" column to tweet_id and change datatype to String.
# 
# 2.**tweet_json:** We only need favorite_count, retweet count,id "tweet_id" (after renamed), columns.

# ### Issue #11:
# rename "id" column to tweet_id and change datatype to String.

# #### Define 
# Rename column id to tweet_id and change its type to String.

# #### Code

# In[41]:


tweet_json_clean.dtypes


# In[42]:


tweet_json_clean = tweet_json_clean.rename(columns={'id': 'tweet_id'})
tweet_json_clean.tweet_id =tweet_json_clean.tweet_id.astype(str) 


# #### Test

# In[43]:


tweet_json_clean.dtypes


# ### Issue #12:
#  We only need favorite_count, retweet count,id "tweet_id" (after renamed), columns.

# #### Define 
# drop all unnecessary column to merge all dataset together later.

# #### Code

# In[44]:


tweet_json_clean= tweet_json_clean.drop(['contributors', 'coordinates', 'created_at', 'display_text_range', 'entities',
                                         'extended_entities', 'favorited', 'full_text', 'geo', 'id_str',
                                         'in_reply_to_screen_name', 'in_reply_to_status_id', 'in_reply_to_status_id_str', 
                                         'in_reply_to_user_id', 'in_reply_to_user_id_str','is_quote_status', 'lang' ,'place',
                                         'possibly_sensitive', 'possibly_sensitive_appealable', 'quoted_status', 
                                         'quoted_status_id','quoted_status_id_str', 'retweeted', 'retweeted_status', 'source'
                                         ,'truncated'], axis=1)


# #### Test

# In[45]:


tweet_json_clean.dtypes


# ## Storing Data
# Save gathered, assessed, and cleaned master dataset to a CSV file named "twitter_archive_master.csv".

# In[46]:


#create a new dataframe by using method 'merge' to merge two dataset 
twitter_archive_master = pd.merge(twitter_archive_clean, 
                      image_predictions_clean, 
                      how = 'left', on = ['tweet_id'])


# In[47]:


twitter_archive_master = pd.merge(twitter_archive_master, tweet_json_clean, 
                      how = 'left', on = ['tweet_id'])


# In[48]:


#check the new dataframe
twitter_archive_master.info()


# ## Analyzing and Visualizing Data
# In this section, analyze and visualize your wrangled data. You must produce at least **three (3) insights and one (1) visualization.**

# ### Insight 1: 

# In[49]:


#calculate the average retweet_count for each type of breeds of dogs.
the_data = twitter_archive_master.groupby('breed_of_dog')['retweet_count'].mean().sort_values()
the_data


# * The breed of dogs that got the highest average in retweets is Bedlington_terrier with 7510 retweet in average.
# 
# * Where as the breed of dog that got the lowest retweet average is groenendael with 276 retweet in average.

# ### Insight 2 & Visualization : 

# In[50]:


#Calculate the average favorite_count for each type of breeds of dogs.
the_data2 = twitter_archive_master.groupby('breed_of_dog')['favorite_count'].mean().sort_values()
the_data2


# * The breed of dogs that got the highest average in favorites is Saluki with 24060 favorites in average.
# 
# * Where as the breed of dog that got the lowest retweet average is brabancon_griffon with 885 retweet in average.
# 
# * it appears that there is a strong relationshipt between retweet_count and favorite_count for the tweet, since that the breed with least average in retweets came second to last for favorite_count and same for the highest average in tweets came the second highest average in favorite count. will try to confirm that in the next two cells.

# In[51]:


#calculate the correlation coeffecint between retweet_count and favorite_retweet.
r = np.corrcoef(twitter_archive_master['retweet_count'], twitter_archive_master['favorite_count'])
#show it in the console
r


# In[52]:


#regplot method is used to plot data and a linear regression model fit,,
#There are a number of mutually exclusive options for estimating the regression model. source(geeksforgeeks)
sb.regplot(x="retweet_count", y="favorite_count", data=twitter_archive_master)


# - ##### With correlation coefficient equals to 0.91 and a positIve strong relationship between retweet_count and favorite_count, there is definitely a  relationship between these two column.

# # Insight 3 & Visualization

# In[53]:


#plotting the distribution of source of tweets.
plot = twitter_archive_master.source.value_counts().plot.pie(figsize=(7, 7),autopct='%.f%%', shadow=True)
plot.set_title('ditribution of source')


# - As we can see in pie plot above, 94% of tweets in this dataset came from twitter for iPhone, which is an indicator that twitter in mobiles in general is where most of users uses the application.

# ## Insight 4 & Visualization

# In[54]:


#plot the distribution of dog_stage in this dataset.
plot2 = twitter_archive_master.dog_stage.value_counts().plot.pie(figsize=(7, 7),autopct='%.f%%', shadow=True)
plot2.set_title('ditribution of the dog stage')


# - 65% of dogs are pupper dogs, and 25% are doggo dogs.

# ### Visualization

# In[55]:


#calculate the average of rating numerator for each type of breeds of dogs.
breeds_of_dog = twitter_archive_master.groupby(['breed_of_dog'])['rating_numerator'].mean().plot(kind='bar', figsize=(10,6),                                                                                                   color="indigo", fontsize=13);

#set the labels and title
breeds_of_dog.set_title("The Average rating numerator for breeds of dogs", fontsize=15)
breeds_of_dog.set_ylabel("average rating numerator", fontsize=15);
plt.show()


# ##### Since we have so many breeds, we need to simplify the graph in order to see it probably.

# In[61]:


#calculate the average count for each breed of dogs
twitter_archive_master['breed_of_dog'].value_counts().mean()


# In[64]:


#source of filter method 'https://stackoverflow.com/questions/13167391/filtering-grouped-dataframe-in-pandas'
#take only breeds that have more than 15 records
filtered_breed = twitter_archive_master.groupby(['breed_of_dog']).filter(lambda x: len(x) > 15)

#plot the average rating for each breed.
xx= filtered_breed.groupby(['breed_of_dog'])['rating_numerator'].mean().plot(kind='bar', figsize=(10,4), color="indigo", fontsize=8);

#set the labels and title
xx.set_title("The Average rating numerator for breeds of dogs", fontsize=10)
xx.set_ylabel("Average rating numerator", fontsize=10);

#calculate the average of rating for filtered_breed 
mean_rating= filtered_breed['rating_numerator'].mean()

#plot a red line that represent the average rating for all breeds of dogs 
plt.axhline(mean_rating, color="r");


# **After filtering , we can see clearly the average rating for each type of breeds.**
# 
# **Also, most of breeds are close the average with an exception for lakeland_terreir.**

# ### Insight 5

# In[58]:


twitter_archive_master.describe()


# - The average favorites is 8779 whereas the retweets is 2768 which shows that users tend to press the like button more often than the retweets, which is obvious since it an account for dog’s fans and like button is a gesture to indicate you like the dog.
# - The average rating numerator is 12.68/10.

# In[59]:


#saving our cleaned and merged dataset: -

#         * I comment this line to avoid saving the file multiple times.

#twitter_archive_master.to_csv('twitter_archive_master.csv', index=True)


# In[ ]:




