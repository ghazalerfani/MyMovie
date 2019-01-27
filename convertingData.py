## Python Project - Section A2 Group 1 - MyMovie
## This is ConvertingData. This file contains helper methods for cleaning and combining the scraped data, as well as 
	## giving the user options to scrape data based on how much time they have
## Made by Shayne Bement, Jeff Curran, Ghazal Erfani, Naphat Korwanich, and Asvin Sripraiwalsupakit
## Imported by myMovie and Imports scrapingMethods

from imdb import IMDb
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import scrapingMethods

ia = IMDb()

##completely rescrapes the data. This means it pings the api (which takes 4 hours), scrapes the wikipedia data,
	## and scrapes the budget and gross datas
def fullScrape():
    actorDf = actorDfGet()
    scrapeData = scrapingMethods.scrapeAll()
    imdbIds = getImdbIds(scrapeData)
    imdbData = pingImdbApi(imdbIds)
    finalData = awardWinningAdd(imdbData, actorDf)
    
    finalData.columns = ['Movie', 'ImdbID', 'Release Date', 'Release Year', 'Actors',
       'award_winning']
    finalData['Release Year'] = [str(i) for i in finalData['Release Year'] ]
    outPut = pd.merge(scrapeData, finalData, on = ['Movie','Release Year'])
    outPut = outPut.drop(['Release Date_x','Release Date_y', 'ImdbID', 'Actors'], axis = 1)
    outPut = outPut.drop_duplicates()
    outPut = outPut[outPut.Genre != ""]
    outPut = outPut.reset_index(drop=True)
    
    ##add some extra analysis columns
    genres = {outPut.Genre.unique()[i] : i for i in range(len(outPut.Genre.unique()))}
    outPut['Genre_Number'] = [genres[outPut.Genre[i]] for i in range(len(outPut))]
    
    distributors = {outPut.Distributor.unique()[i] : i for i in range(len(outPut.Distributor.unique()))}
    outPut['Distributor_Number'] = [distributors[outPut.Distributor[i]] for i in range(len(outPut))]

    mpaa = {outPut.MPAA.unique()[i] : i for i in range(len(outPut.MPAA.unique()))}
    outPut['MPAA_Number'] = [mpaa[outPut.MPAA[i]] for i in range(len(outPut))]
    
    outPut.to_csv("data/processed/FullOutput.csv")
    return outPut
    
    
##The quickest scrape, basically just loads in the default dataset for analysis     
def noScrape():
    imdbData = pd.read_csv("data/processed/FullOutput.csv")
    imdbData = imdbData.drop('Unnamed: 0', axis = 1)
    return imdbData
    
##A quicker version of scraping. Cuts out the api call, but rescraping the budget, wikipedia, and budget data.
	## This version only takes about 5 minutes.
def quickScrape():
    actorDf = actorDfGet()
    scrapeData = scrapingMethods.scrapeAll()
    imdbData = pd.read_csv("data/processed/APICallResults.csv")
    finalData = awardWinningAdd(imdbData, actorDf)
    
    finalData.columns = ['Movie', 'ImdbID', 'Release Date', 'Release Year', 'Actors',
       'award_winning']
    finalData['Release Year'] = [str(i) for i in finalData['Release Year'] ]
    outPut = pd.merge(scrapeData, finalData, on = ['Movie','Release Year'])
    outPut = outPut.drop(['Release Date_x','Release Date_y', 'ImdbID', 'Actors'], axis = 1)
    outPut = outPut.drop_duplicates()
    outPut = outPut[outPut.Genre != ""]
    outPut = outPut.reset_index(drop=True)
    
    
    ##add some extra analysis columns
    genres = {outPut.Genre.unique()[i] : i for i in range(len(outPut.Genre.unique()))}
    outPut['Genre_Number'] = [genres[outPut.Genre[i]] for i in range(len(outPut))]
    
    distributors = {outPut.Distributor.unique()[i] : i for i in range(len(outPut.Distributor.unique()))}
    outPut['Distributor_Number'] = [distributors[outPut.Distributor[i]] for i in range(len(outPut))]

    mpaa = {outPut.MPAA.unique()[i] : i for i in range(len(outPut.MPAA.unique()))}
    outPut['MPAA_Number'] = [mpaa[outPut.MPAA[i]] for i in range(len(outPut))]

    outPut.to_csv("data/processed/FullOutput.csv")
    return outPut
    

## Gets the raw actor award data, which was one of our downloaded sources    
def actorDfGet():   
    ##first load and cut down our raw award data
    rawDf = pd.read_csv("data/raw/rawAwardData.csv")
    rawDf.Winner.fillna(0.0)

    keepCats = ['Actor', 'Actress','Actor in a Supporting Role', 'Actress in a Supporting Role','Actor in a Leading Role', 'Actress in a Leading Role']
    actors = rawDf[rawDf.Award.isin(keepCats)]
    actorWinners = actors[actors.Winner > 0]
    actorWinners = actorWinners[[not i for i in pd.Series(actorWinners.Name).duplicated()]]
    actorWinners = actorWinners.reset_index(drop=True)

    for i in range(len(actorWinners)):
        row = actorWinners.iloc[i].Year.split("/")
        if len(row) > 1:
            actorWinners.at[i,'Year'] = int(row[1])
        else:
            actorWinners.at[i,'Year'] = int(actorWinners.at[i,'Year'])
    return actorWinners



##load metadata on imdb data
def getImdbIds(masterDat):
    metaData = pd.read_csv("data/raw/movies_metadata.csv")
    metaData = metaData[['title', 'imdb_id', 'release_date']]
    metaData  = metaData[[not i for i in pd.isna(metaData.release_date.values)]]

    yearGood = [i for i in range(1995,2019)]
    metaData = metaData[[any([str(i) in str(year) for i in yearGood]) for year in metaData.release_date.values]]

    yearCol = []
    for i in metaData.release_date.values:
        yearCol.append(int(str(i).split('/')[2]))

    metaData['year'] = yearCol
    metaData = metaData[[not i for i in pd.isna(metaData.imdb_id.values)]]
    overLapSet = metaData[[i in masterDat.Movie.values for i in metaData.title]]
    return overLapSet


##api call, takes 4 hours roughly
def pingImdbApi(dataSet):    
    dataSet = dataSet[[not i for i in pd.isna(dataSet.imdb_id.values)]]
    imdb_id = []
    ##get just the code segment of our imdb codes
    for i in dataSet.imdb_id.values:
        imdb_id.append(i.split("tt")[1])

    results = []
    imdb_idtrack = []
    for j in imdb_id:
        names = 'NaN'
        movie = ia.get_movie(j)
        if movie.get('cast') != None:
            print(str(len(results)), " of ", str(len(imdb_id)))
            names = movie.get('cast')
            results.append([names[i]['name'] for i in  range(len(names))])
            imdb_idtrack.append([i for i in range(len(names))])
        else: results.append([np.nan])

    temp_frame = pd.DataFrame({'a':results})
    ApiResults = pd.concat([dataSet,temp_frame], ignore_index=True, axis=1)

    ##remove any movies without actors
    ApiResults = ApiResults[[not pd.isna(ApiResults.loc[x][0][0]) for x in range(len(ApiResults))]]
    ApiResults = ApiResults.reset_index(drop=True)
    ##make columns more intruitively named
    ApiResults=ApiResults.rename(index = str, columns = {0:'Movie', 1: 'ImdbID',2:'Release_Date',3:'Release_Year',4:'Actors'})
    ApiResults.to_csv("data/processed/APICallResults.csv", index = False) 
    return ApiResults


## maps our award winners to the movie dataset, replacing actors with a flag for if the film had
## any award winning actors
def awardWinningAdd(apiResults, actorWinners):
    print("Mapping award winning actors to movies")
    apiResults['award_winning'] = [0  for i in range(len(apiResults.Title))]
    for i in range(len(actorWinners)):
        actorRow = actorWinners.iloc[i]
        name = actorRow.Name
        year = actorRow.Year
        apiResults.loc[[(name in apiResults.Actors[i]) & (apiResults.Release_Year[i] > year)
                        for i in range(len(apiResults))], 'award_winning'] = 1
    return apiResults
