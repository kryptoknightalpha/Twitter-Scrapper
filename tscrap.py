"""
Python Script to scrape tweets from Twitter with python through the Twitter Search (Rest) API.
I designed it to search twitter for various keywords tweeted by users and return the result in table.
"""

import pandas as pd
from datetime import date, datetime
import sys
import base64
import requests
import re

def getUserName():
    while True:
        try:
            username = input("Enter the Twitter usernames you'd like to track, seperated by a comma (example: @Username1, @Username2):")
            if username[0][0] != '@':
                raise ValueError
            else:
                userList = username.replace(" ", "").replace("@", "from:@").replace(",", " OR ")

            return userList
        except ValueError:
            print("Hmmm... " + username + " do not look like a valid usernames. Let's try that again.")


def getKeyWords():
    while True:
        try: 
            keywords = input("Enter the keywords you'd like to track, seperated by a comma (example: stealth, action): ")
            keywords = keywords.replace(", ", ",").split(",")
            
            for keyword in keywords:
                if (" ") in keyword:
                    raise ValueError # this will send it to the print message and back to the input option            
            
            keywords = " OR ".join(keywords)
            return keywords
        
        except ValueError:
            print("Hmmm...keywords can only be single words, not phrases. Let's try that again.")


def getBlackListWords():
    while True:
        try: 
            blacklistWords = input("Enter the words you'd like to avoid in your search, seperated by a comma (example: Stealth, action): ")
            blacklistWords = blacklistWords.replace(", ", ",").split(",")
            
            for word in blacklistWords:
                if (" ") in word:
                    raise ValueError # this will send it to the print message and back to the input option  
            
            blacklistWords = " -".join(blacklistWords)
            blacklistWords = "-" + blacklistWords
            return blacklistWords
        
        except ValueError:
            print("Hmmm...blacklistWordsed words can only be single words, not phrases. Let's try that again.")




def format_usernames():
   
   # Format usernames for search
   usernames = user['usernames'][0]
   usernames = usernames.replace(" ", "").split("OR")
   
   # Organize first set of usernames
   usernames_one = usernames[0]
   for item in usernames[1:11]:
       usernames_one += ' OR ' + item
       
   # Organize second set if > 11 usernames   
   try: 
       usernames_two = usernames[11]
   
       for item in usernames[12:23]:
           usernames_two += ' OR ' + item

   except IndexError:
       usernames_two = []
       
       
   # Organize second set if > 24 usernames    
   try: 
       usernames_three = usernames[23]
   
       for item in usernames[24:35]:
           usernames_three += ' OR ' + item

   except IndexError:
       usernames_three = []
       
       
   # Organize second set if > 36 usernames   
   try: 
       usernames_four = usernames[35]
   
       for item in usernames[36:47]:
           usernames_four += ' OR ' + item

   except IndexError:
       usernames_four = []
       
       
    # Organize second set if > 48 usernames   
   try: 
       usernames_five = usernames[47]
   
       for item in usernames[48:59]:
           usernames_five += ' OR ' + item

   except IndexError:
       usernames_five = []
              
       
    # Organize second set if > 60 usernames   
   try: 
       usernames_six = usernames[59]
   
       for item in usernames[60:71]:
           usernames_six += ' OR ' + item

   except IndexError:
       usernames_six = []
       
   return usernames_one, usernames_two, usernames_three, usernames_four, usernames_five, usernames_six





if __name__ == "__main__":
    try:
        user = pd.read_csv("twitter_settings.csv", index_col=0)
        keywords = user['keywords'][0]
        blacklist = user['blacklist'][0]
        
        usernames_one, usernames_two, usernames_three, usernames_four, usernames_five, usernames_six = format_usernames()
    

    except IOError:
        
        print("Let's get you setup!")
        
        # Get Scrape Settings
        usernames = getUserName()
        keywords = getKeyWords()
        blacklist = getBlackListWords()
        date = date.today().strftime('%Y-%m-%d')
        filename = sys.argv[0]
        
        # create user dataframe
        col = {"usernames":usernames, "keywords":keywords, "blacklist":blacklist}
        user = pd.DataFrame(col, index= [date])
        user.to_csv("twitter_settings.csv", encoding='utf-8', index=True)
        
        usernames_one, usernames_two, usernames_three, usernames_four, usernames_five, usernames_six = format_usernames()
            
        print("Your twitter settings are all setup! You can edit these search settings directly through the file named 'twitter_settings.csv'. You can find this file at " + filename)

    try:
        f= open("credentials.txt","r")
        client_key = contents.replace("=",",").split(",")[1]
        client_secret = contents.replace("=",",").split(",")[3]
    except:
        f= open("credentials.txt","w+")
        client_key = input('Client Key: ')
        client_secret = input('Client Secret: ')
        f.write("client_key={}, client_secret={}".format(client_key,client_secret))
        f.close()

    #Reformat the keys and encode them
    key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')

    # Transform from bytes to bytes that can be printed
    b64_encoded_key = base64.b64encode(key_secret)

    #Transform from bytes back into Unicode
    b64_encoded_key = b64_encoded_key.decode('ascii')

    #Adding authorization to base URL 

    base_url = 'https://api.twitter.com/'
    auth_url = '{}oauth2/token'.format(base_url)

    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}

    auth_data = {
        'grant_type': 'client_credentials'}

    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)


    #Creating bearer token

    access_token = auth_resp.json()['access_token']

    search_headers = {
        'Authorization': 'Bearer {}'.format(access_token)}



    def Call_api(username_group):

        #Adding search parameters: ('OR' = or)('+' = and)('-' = not) *(space interpreted as &)

        search_params = {'q': username_group + " + " + keywords + " + " + blacklist,}

        #Adding Twitter search API to base URL
        search_url = '{}1.1/search/tweets.json'.format(base_url)

        #Putting all elements together and execute request 
        resp = requests.get(search_url, headers=search_headers, params=search_params)


        #Get the data from the 1st request
        import json
        scrape = json.loads(resp.content)
        
            #Extracting desired data from 1st scrape as lists
        users = []
        tweet_dates = []
        kw_tweets = []


        for tweet in scrape['statuses']:
            users.append(tweet['user']['screen_name'])
            kw_tweets.append(tweet['text'])
            dates = datetime.strptime(tweet['created_at'][4:-11], '%b %d %H:%M:%S').strftime('%m/%d %H:%M')
            tweet_dates.append(dates)
            
            
        #Creating df1 via pandas
        #Creating columns names and adding their data
        scrape = {
            "User" : users,
            "Date" : tweet_dates,
            "Tweet" : kw_tweets,   
        }

        #Create DataFrame
        df = pd.DataFrame(scrape)
        return df



    DataFrame = Call_api(usernames_one)

    if usernames_two != []:
    
        df = Call_api(usernames_two)
        
        DataFrame = pd.concat([DataFrame,df], ignore_index=True)
    elif usernames_three != []:
        df = Call_api(usernames_three)
        
        DataFrame = pd.concat([DataFrame,df], ignore_index=True)
    elif usernames_four != []:
        df = Call_api(usernames_four)
        
        DataFrame = pd.concat([DataFrame,df], ignore_index=True)
    elif usernames_five != []:
        df = Call_api(usernames_five)
        
        DataFrame = pd.concat([DataFrame,df], ignore_index=True)
    elif usernames_six != []:
        df = Call_api(usernames_six)
        
        DataFrame = pd.concat([DataFrame,df], ignore_index=True)
    else:
        pass

    DataFrame

    DataFrame['Tweet'].replace('(https://t.co)/(\w+)', r'\1', regex=True).drop_duplicates()
    tweets = DataFrame.loc[DataFrame['Tweet'].replace('(https://t.co)/(\w+)', r'\1', regex=True).drop_duplicates().index]
    tweets = tweets.sort_values(by=['Date'], ascending=False)
    tweets.reset_index(drop=True, inplace=True)
    tweets

    #Export data to CSV file
    tweets.to_csv("kw_tweets.csv", encoding='utf-8', index=False)


"""
  #Export table to Excel without index column
    writer = pd.ExcelWriter("kw_tweets.xlsx", engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.save()   
"""
