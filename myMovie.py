# Python Project - Section A2 Group 1 - MyMovie
##This is the myMovie script. This is the main script for our application. It gets user input to run through our regression models, and can display visual historical data	
	## for the user to have or use as a reference.
## Made by Shayne Bement, Jeff Curran, Ghazal Erfani, Naphat Korwanich, and Asvin Sripraiwalsupakit
## Imports convertingData, Simple_Regression_Models, and KNN_DecisionTree_Regressions_Models

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys

import convertingData
import Simple_Regression_Models as srm
import KNN_DecisionTree_Regressions_Models as kdrm

# main DataFrame is called dataset
try:
    dataset = pd.read_csv('data/processed/FullOutput.csv')
except FileNotFoundError:
    ans = input("Looks like it's your first time running MyMovie.\nWould you like to \
initialize your movie database? [Y/N]\n(NOTE: this will take approx. 6 hours!)")
    if (ans == 'Y' or ans == 'y'):
         dataset = convertingData.fullScrape()
    else:
        print('Goodbye!')
        sys.exit()
    
# lists and dict for user input
genrelist = dataset.Genre.unique().tolist()
mpaalist = dataset.MPAA.unique().tolist()

# import necessary files for visualization
#read csv
df_link = pd.read_csv('data/raw/links.csv')
df_movies = pd.read_csv('data/raw/movies.csv')
df_ratings = pd.read_csv('data/raw/ratings.csv')

#merge table
pd.merge(df_link, df_movies)
df_movie_count = pd.DataFrame(df_ratings.groupby('movieId').count()[['userId']])
df_movie_mean = pd.DataFrame(df_ratings.groupby('movieId').mean()[['rating']])
df_rating_sum = pd.merge(df_movie_count,df_movie_mean ,left_index=True, right_index=True , how = 'left')
df_movielens = df_movies.join(df_rating_sum, on = 'movieId')

#generate distinct genre
genre = []
for v in df_movielens['genres']:
    a = v.split('|')
    for v2 in a:
        if v2 not in genre:
            genre.append(v2)
            
#generate distinct genre
movie_list = pd.DataFrame(columns=['movieId','title','genre','avg_rating','count_raters'])
i = 0
for index, row in df_movielens.iterrows():
    if(i<1000 ):
        a = row['genres'].split('|')
        for v2 in a:
            movie_list.loc[i] = [round(row['movieId'],0),row['title'],v2,row['rating'],row['userId']]
            i+=1

def visualize_menu():
    loop = True
    while loop:
        print("""\n  Select historical data to explore
    1. Movie rating by genre
    2. Movie budget & revenue analysis
    3. Quit""")
        
        ans = input('Enter your option: ') 
        print('**************************') 
        
        if ans == '1':
            rating_by_genre_plot()
            loop = False
        if ans == '2':
            butget_analysis()
            loop = False
        if ans == '3': 
            print('\n Goodbye!') 
            loop = False

def rating_by_genre_plot():
    #show the box plot of the average rating of the movies in each genre 
    print('Box plot of the average rating of the movies in each genre')
    sns.boxplot(y='genre', x='avg_rating',data = movie_list).set_title('Rating Distribution by Genre')
    plt.show()
    
    #print menu
    print('Select the genre to see top rated movie under each genre')
    print('-----------------------------------')

    i = 0
    for a,b,c in zip(genre[::3],genre[1::3],genre[2::3]):        
        print('{:<3}{:<30}{:<3}{:<30}{:<3}{:<}'.format(i,a,i+1,b,i+2,c))
        i += 3
    answer = input('    Your choice: ').strip()
    genre_selected = genre[int(answer)]
    print('Genre selected: ',genre_selected)

    #Retrieve movie list for the selected genre
    movie_list_genre = pd.DataFrame(columns=['movieId','title','avg_rating','count_raters'])
    i = 0

    for index, row in df_movielens.iterrows():
        if genre_selected in row['genres']:
            movie_list_genre.loc[i] = [round(row['movieId'],0),row['title'],row['rating'],row['userId']]
            i += 1

    #Sort the list by rating, and filter for movies with raters number higher than 100
    movie_list_genre = movie_list_genre.sort_values(by=['avg_rating'],ascending=[0])
    movie_list_genre = movie_list_genre[movie_list_genre['count_raters']>100]
    #movie_list_genre[:10]

    #show the top rating movie of the selected genre
  
    print('Top rated movie in ',genre_selected)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14,20))
    movie_list_genre_top10 = movie_list_genre.iloc[:20]
    sns.barplot(data = movie_list_genre_top10, y = movie_list_genre_top10['title']
                , x = movie_list_genre_top10['avg_rating'], ax = ax1).set_title('Top Movies by Rating')

    #Sort the list by popularity
    movie_list_genre_pop = movie_list_genre.sort_values(by=['count_raters'],ascending=[0])
    movie_list_genre_pop_top10 = movie_list_genre_pop.iloc[:20]
    sns.barplot(data = movie_list_genre_pop_top10, y = movie_list_genre_pop_top10['title']
                , x = movie_list_genre_pop_top10['count_raters'], ax = ax2).set_title('Top Movies by Number of Raters')
    fig.suptitle('Top 20 movies based on rating and popularity',size=25)
    plt.show()

    #show the distribution of the average rating of the movies in the selected genre 
    values = pd.Series(movie_list_genre['avg_rating'])
    sns.boxplot(values).set_title('Distribution of the average rating of the movies\n in the selected genre')
    plt.show()
    
def butget_analysis():
    df2 = pd.DataFrame(columns=['Budget','Revenue','Genre','Release Year'], dtype = float)
    loop = 0
    while loop < 2863:
        df2.loc[loop] = [dataset.loc[loop]['Production_Budget']
                         ,dataset.loc[loop]['Worldwide_Gross']
                         ,dataset.loc[loop]['Genre_Number']
                        ,str(dataset.loc[loop]['Release Year'])]
        loop+=1
    c = pd.DataFrame([df2.groupby(['Release Year']).mean()['Revenue'], df2.groupby(['Release Year']).mean()['Budget']])
    c = c.transpose()

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16,4))

    c['Revenue'].plot.bar(title = 'Average Revenue per Movie Trends \n (100 million)', ax = ax1)
    c['Budget'].plot.bar(title = 'Average Production Budget per Movie Trends \n(10 million)', ax = ax2)
    c.loc[:, 'Revenue':'Budget'].plot(title = 'Average Revenue and Budget Trend\n (100 million)', ax = ax3)
    plt.show()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14,8))
    sns.boxplot(x='Genre', y='Budget',data = df2, ax = ax1).set_title('Production Budget by Genre (100 million)')
    plt.ylim(10, 1000000000)
    sns.boxplot(x='Genre', y='Revenue',data = df2, ax = ax2).set_title('\nRevenue by Genre (1000 million)')
    plt.ylim(10, 1000000000)
    plt.show()

### Main Menu
print('*** Welcome to MyMovie ***')
print('Empower producers to make successful movies')
print('**************************')

print("""Do you want to continue from saved dataset or fetch new data?
    1. Continue without fetching new data
    2. Partially fetching 
    3. Full fetching (approx. 6 hrs)
""")
check_input = True
while(check_input):
    try:
        option = input('Select option 1, 2, or 3: ')
        if (option == '1' or option == '2' or option == '3'):
            check_input = False
            dataset = convertingData.noScrape()
        if (option == '2'):
            check_input = False
            dataset = convertingData.quickScrape()
        if (option == '3'):
            check_input = False
            dataset = convertingData.fullScrape()
    except:
        print('Please select option 1, 2, or 3')
        check_input = True    

# Converting $ to int before calling regression
production_budget = []
for s in dataset['Production_Budget']:
    s = s[1:]
    f = int(s.replace(',', ''))
    production_budget.append(f)
dataset['Production_Budget'] = production_budget

worldwide_gross = []
for s in dataset['Worldwide_Gross']:
    s = s[1:]
    f = int(s.replace(',', ''))
    worldwide_gross.append(f)
dataset['Worldwide_Gross'] = worldwide_gross
           
# Application's main menu: looping main menu options to collect five parameters for regression, 
# or allow user to select visualization (of historical data) to view        
loop = True
while loop:
    print ("""Main Menu
    1. Revenue Forecast
    2. Explore Historical Data
    3. About
    4. Quit""")

    ans = input('Enter your option: ') 
    print('**************************')
    if ans == '1': 
        loop = False
        print('Please enter the following information to forecast movie revenue\n')
        
        # Get genre selection of user
        print('Select genre')
        i = 1
        for a,b,c in zip(genrelist[::3],genrelist[1::3],genrelist[2::3]):        
            print('{:<3}{:<30}{:<3}{:<30}{:<3}{:<}'.format(i,a,i+1,b,i+2,c))
            i += 3
        
        check_input = True
        while(check_input):
            try:
                genreint = int(input('Enter number corresponding to genre: '))
                genreint -= 1
                check_input = False
                if (genreint < 0 or genreint > len(genrelist)):
                    check_input = True
                    print('Integer input must be within the range of genre name')
            except:
                print('Please enter an integer corresponding to genre name')
                check_input = True               
                

        # Get MPAA rating selection of user
        print('\nSelect MPAA rating')
        i = 1
        for a,b,c in zip(mpaalist[::3],mpaalist[1::3],mpaalist[2::3]):        
            print('{:<3}{:<30}{:<3}{:<30}{:<3}{:<}'.format(i,a,i+1,b,i+2,c))
            i += 3
        
        check_input = True
        while(check_input):
            try:
                mpaaint = int(input('Enter number corresponding to MPAA rating: '))
                mpaaint -= 1
                check_input = False
                if (mpaaint < 0 or mpaaint > len(genrelist)):
                    check_input = True
                    print('Integer input must be within the range of MPAA rating')
            except:
                print('Please enter an integer corresponding to MPAA rating')
                check_input = True        
                
        # Get estimated production budget from user
        check_input = True
        while(check_input):
            try:
                budget = int(input('\nEnter estimated production budget: $ '))
                check_input = False
                if (budget < 0):
                    check_input = True
                    print('Budget must be positive value')
            except:
                print('Please enter budget amount without thousands separator')
                check_input = True    
        
        # Get 'based on book' info from user
        check_input = True
        while(check_input):
            try:
                is_book = input('\nIs this movie based on a book? (y/n) ')
                if (is_book == 'y' or is_book == 'n'):
                    check_input = False
                    if (is_book == 'y'):
                        is_book = 1
                    if (is_book == 'n'):
                        is_book = 0
                else:
                    print('Please enter a single character \'y\' or \'n\'')
            except:
                print('Please enter a single character \'y\' or \'n\'')
                check_input = True    
                
        # Get 'has award' info from user
        check_input = True
        while(check_input):
            try:
                has_award = input('\nDoes the movie consist of award winning actor/actress? (y/n) ')
                if (has_award == 'y' or has_award == 'n'):
                    check_input = False
                    if (has_award == 'y'):
                        has_award = 1
                    if (has_award == 'n'):
                        has_award = 0
                else:
                    print('Please enter a single character \'y\' or \'n\'')
            except:
                print('Please enter a single character \'y\' or \'n\'')
                check_input = True
                
    elif ans=='2':
        loop = False
        visualize_menu()
    elif ans == '3':
        print('About')
        print('''This compact application aims to help empowering producers to make successful movies based on publicly 
available historical data through our regression model, and allowing users to explore information and
figures related to past successful films. Created for 95888 Data Focused Python Course in Fall 2018 - 
Heinz College, Carnegie Mellon University''') 
        print('**************************') 
    elif ans == '4':
        print('\n Goodbye!') 
        loop = False
    elif ans !='':
        print('\n Invalid Input. Please try again')


##### Call Prediction Models ####
user_input = []
if (ans == '1'):
    user_input = [genrelist[genreint], mpaalist[mpaaint], budget, is_book, has_award]

    grossEarnings, errorTerm = srm.LinearRegression(dataset, user_input)
    logGrossEarnings, logErrorTerm = srm.LogisticRegression(dataset, user_input)
    budgetEarnings, budgetErrorTerm = srm.BudgetOnlyRegression(dataset, user_input)
    grossEarningsRange, errorRangeTerm = kdrm.KNN_Regression(dataset, user_input)
    grossTreeEarnings, errorTreeTerm = kdrm.DecisionTree_Regression(dataset, user_input)

    print('\nLinear Regression Model')
    print('Projected Budget: ', "${:,}".format(user_input[2]))
    print('Predicted Gross Budget: ', "${:,}".format(grossEarnings))
    print('predicted Root Mean Squared Error: ', "${:,}".format(errorTerm))
 
    print('\nLinear Regression Model (Budget Only)')
    print('Projected Budget: ', "${:,}".format(user_input[2]))
    print('Predicted Budget Gross Budget: ', "${:,}".format(budgetEarnings))
    print('predicted Budget Root Mean Squared Error: ', "${:,}".format(budgetErrorTerm))
 
    print('\nLogistic Regression Model')
    print('Projected Budget: ', "${:,}".format(user_input[2]))
    print('Predicted Gross Budget: ', "${:,}".format(logGrossEarnings))
    print('predicted Root Mean Squared Error: ', "${:,}".format(logErrorTerm))
 
    print('\nKNN Regression Model')
    print('Projected Budget: ', "${:,}".format(user_input[2]))
    print('Predicted Gross Budget: ', "${}".format(grossEarningsRange))
    print('predicted Root Mean Squared Error: ', "{:,}".format(errorRangeTerm), ' bins')
     
    print('\nDecision Tree Model')
    print('Projected Budget: ', "${:,}".format(user_input[2]))
    print('Predicted Budget Gross Budget: ', "${:,}".format(grossTreeEarnings))
    print('predicted Budget Root Mean Squared Error: ', "${:,}".format(errorTreeTerm))

