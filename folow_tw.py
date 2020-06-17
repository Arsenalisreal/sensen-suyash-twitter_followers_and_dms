import tweepy
import pandas as pd
import json
import operator 
import csv


consumer_key = 'QJW90qPAXY9BiIfVEVWVvI6kB'
consumer_secret = '4Aefi4H0nmZLICKZd2mNWXlyHaVM4X3zmRHsgGditDDSUhMPtR'
access_token = '1272755570974441474-b1dMAUvTY8oZRNkpg3hskKlbVGM95b'
access_token_secret = 'm9av3bNzA5kTbHZ0zlMc77eqf7DYanh0TI8SLaXZ2zIsm'


print('begin')

def lookup_user_list(user_id_list, api):
    full_users = []
    users_count = len(user_id_list)
    try:
        for i in range(round(users_count / 100) + 1):
            print(i)
            full_users.extend(api.lookup_users(user_ids=user_id_list[i * 100:min((i + 1) * 100, users_count)]))
        return full_users
    except tweepy.TweepError:
        print('Something went wrong, quitting...')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 

# set access to user's access key and access secret 
auth.set_access_token(access_token, access_token_secret) 

# calling the api 
api = tweepy.API(auth) 
ids = []
for page in tweepy.Cursor(api.followers_ids, screen_name="Chamarthysuyash").pages():
    ids.extend(page)

results = lookup_user_list(ids, api)
all_users = [{'id': user.id,
             'Name': user.name,
             'Statuses Count': user.statuses_count,
             'Friends_Count': user.friends_count,
             'Screen Name': user.screen_name,
             'Followers Count': user.followers_count,
             'Description': user.description}
             for user in results]

df = pd.DataFrame(all_users)

# sorting them based on number of accounts each is following
#sort=sorted(df,key=operator.itemgetter(2))

df.to_csv('D:\\linking\\scripts\\intern2\\All_followers.csv', index=False, encoding='utf-8')
get_id=df.Friends_Count
sort_orders = sorted(get_id.items(), key=lambda x: x[1], reverse=True)

for i in sort_orders:
	print(df.Name[i[0]]+' follows '+ str(i[1])+' page(s)')

#IMPORTANT note: do not forget to change the permissions while generating the secret token
# Permissions have to be set to read, write, and diremact message 

x=[]
y=[]
# reading the required parameters
with open('D:\\linking\\scripts\\intern2\\All_followers.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        x.append(row['id'])
        y.append(row['Name'])


# assign the values accordingly 


# authorization of consumer key and consumer secret 


# sending messages till the limit is exhausted
ct=0 # only 1000 dms are allowed for each account in 24hrs. 
while ct<1000:
    for i in range(len(x)):
        rec_id=x[i]
        msg="Hi,"+y[i]+" hope your are doing well"
        direct_message=api.send_direct_message(rec_id,msg)
        print(direct_message.message_create['message_data']['text'])
        print('Message sent to '+y[i])
        ct+=1

print("All messages sent.")


