# Python Project - Section A2 Group 1 - MyMovie
##This is the scrapingMethods script. This script contains functions that handle the various potential webscraping actions the program takes. 
## Made by Shayne Bement, Jeff Curran, Ghazal Erfani, Naphat Korwanich, and Asvin Sripraiwalsupakit
## Imported by convertingData

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from urllib.request import urlopen 

##the urls of movie gross sales information since 1995
grossingWebsites = [
    'https://www.the-numbers.com/market/2018/top-grossing-movies',
    'https://www.the-numbers.com/market/2017/top-grossing-movies',
    'https://www.the-numbers.com/market/2016/top-grossing-movies',
    'https://www.the-numbers.com/market/2015/top-grossing-movies',
    'https://www.the-numbers.com/market/2014/top-grossing-movies',
    'https://www.the-numbers.com/market/2013/top-grossing-movies',
    'https://www.the-numbers.com/market/2012/top-grossing-movies',
    'https://www.the-numbers.com/market/2011/top-grossing-movies',
    'https://www.the-numbers.com/market/2010/top-grossing-movies',
    'https://www.the-numbers.com/market/2009/top-grossing-movies',
    'https://www.the-numbers.com/market/2008/top-grossing-movies',
    'https://www.the-numbers.com/market/2007/top-grossing-movies',
    'https://www.the-numbers.com/market/2006/top-grossing-movies',
    'https://www.the-numbers.com/market/2005/top-grossing-movies',
    'https://www.the-numbers.com/market/2004/top-grossing-movies',
    'https://www.the-numbers.com/market/2003/top-grossing-movies',
    'https://www.the-numbers.com/market/2002/top-grossing-movies',
    'https://www.the-numbers.com/market/2001/top-grossing-movies',
    'https://www.the-numbers.com/market/2000/top-grossing-movies',
    'https://www.the-numbers.com/market/1999/top-grossing-movies',
    'https://www.the-numbers.com/market/1998/top-grossing-movies',
    'https://www.the-numbers.com/market/1997/top-grossing-movies',
    'https://www.the-numbers.com/market/1996/top-grossing-movies',
    'https://www.the-numbers.com/market/1995/top-grossing-movies']

##various wikipedia articles to scrape for book based movie information
wikiWebsites = ['https://en.m.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(0%E2%80%939,_A%E2%80%93C)',
            'https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(D%E2%80%93J)',
            'https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(K%E2%80%93R)',
            'https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(S%E2%80%93Z)']

			

##this function scrapes the budget information for a given url. This is a helper function used in the scrapeAll function			
def budgetScrape(webpage):
    soup = BeautifulSoup(webpage.text, 'lxml')

    table = soup.find_all('table')[0]
    numRows = len(table.find_all('tr'))

    movieBudgetDF = pd.DataFrame(columns = ['Release Date', 'Movie', 'Rank', 'Production_Budget', 'Domestic_Gross', 'Worldwide_Gross'], index = range(0, int(numRows/2)))
    
    rowIndex = 0
    for row in table.find_all('tr'):
        if len(row.find_all('a')) == 0:
            continue
        elif rowIndex > 99:
            break
        colIndex = 0
        for column in row.find_all('a'):
            movieBudgetDF.iat[rowIndex, colIndex] = column.get_text()

            colIndex += 1
        colIndex = 2
        for column in row.find_all('td', class_ = 'data'):
            movieBudgetDF.iat[rowIndex, colIndex] = column.get_text()
            colIndex += 1
        rowIndex += 1
        
    return movieBudgetDF
 
 
##Extracts gross information from a given response from scraping a webpage. Called in scrapeAll function
def grossScrape(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find_all('table')[0]

    n_rows = len(table.find_all('tr')) - 2
    df = pd.DataFrame(columns=['Movie', 'Release Date', 'Distributor', 'Genre', 'MPAA', 'Rank in Year Released','2018 Gross', 'Tickets Sold'], index=range(0,n_rows))

    row_number = 0
    for row in table.find_all('tr'):
        column_number = 0
        for column in row.find_all('a'):
            df.iat[row_number,column_number] = column.get_text()
            column_number += 1
        column_number = 5
        for column in row.find_all('td', class_ = 'data'):
            df.iat[row_number,column_number] = column.get_text()
            column_number += 1
        row_number +=1

    df.drop(columns = 'Rank in Year Released')
    df = df.iloc[1:]
    return df


##scrapes the book to movie conversion information from a given wikipedia webpage. Called in scrapeAll function
def WikiScrape(webpage):
    soup = BeautifulSoup(webpage.text, 'lxml')    #html.parser
    
    #Get a list of all wikitable tags
    wikitable_list = soup.find_all('table', { "class" : "wikitable" })
    
    tableIndex = 0
    for table in wikitable_list:
        numRows = len(table.find_all('td')*2)
        bookToMovieDF = pd.DataFrame(columns=['Movie', 'Book'], index = range(0, int(numRows)))
        
        movieIndex = 0
        for row in table.find_all('tr'):
            colIndex = 0
            for column in row.find_all('i'):
                if colIndex == 0:   #populates Book Col
                    book = column.get_text()
                else:   #Creates a list of movies based off the book
                    if column.get_text() not in bookToMovieDF.Movie.values:
                        bookToMovieDF.iat[movieIndex, 0] = column.get_text()
                        bookToMovieDF.iat[movieIndex, 1] = book
                        movieIndex += 1
                colIndex += 1
            
        if tableIndex == 0:
            websiteBookToMovieDF = bookToMovieDF[1:]
        else:
            websiteBookToMovieDF = websiteBookToMovieDF.append(bookToMovieDF[1:], ignore_index = True)
        tableIndex += 1
    websiteBookToMovieDF = websiteBookToMovieDF.dropna(how='all')
    return websiteBookToMovieDF


##Calls all our scrapers and aggregates the data in a way that can be used in the converingData script. 
##Returns a dataframe of movie gross, movie budget, if the movie was based on a book, and other metadata
def scrapeAll():
    budgetDf = pd.DataFrame()
    base = 'https://www.the-numbers.com/movie/budgets/all'
    print("Scraping movie budget data.")
    for i in range(51):
        if i == 0:
            url = base
            budgetDf = budgetScrape(requests.get(url))
        else:
            url = base + '/' +str((i*100)+1)
            budgetDf = budgetDf.append(budgetScrape(requests.get(url)), ignore_index=True)

	##provide some updates on progress so program doesnt appear to be hanging
    print("Scraping book adaptation data.")
    wikiDf = pd.DataFrame()
    index = 0
    for url in wikiWebsites:
        if index == 0:
            wikiDf = WikiScrape(requests.get(url))
        else:
            wikiDf = wikiDf.append(WikiScrape(requests.get(url)), ignore_index = True)
        index += 1

    print("Scraping movie gross data.")
    grossDf = pd.DataFrame()
    for i in grossingWebsites:
        response = requests.get(i)
        if (i == 'https://www.the-numbers.com/market/2018/top-grossing-movies'):
            grossDf = grossScrape(response)
        else:
            grossDf = grossDf.append(grossScrape(response), ignore_index=True)

    print("Combining and cleaning")
    grossWiki = pd.merge(grossDf, wikiDf, on = 'Movie', how='left')
    bookNum = np.array([1 for i in range(len(grossWiki))])
    bookNum[pd.isna(grossWiki.Book)] = 0
    grossWiki['Book_Based'] = bookNum
    fullScrape = pd.merge(grossWiki, budgetDf, on = ['Movie', 'Release Date'])
    fullScrape['Release Year'] = [i.split("/")[2] for i in fullScrape['Release Date']]
    fullScrape = fullScrape.drop(['Rank','Rank in Year Released', 'Book','2018 Gross', 'Tickets Sold', 'Domestic_Gross'], axis = 1)
    return fullScrape


