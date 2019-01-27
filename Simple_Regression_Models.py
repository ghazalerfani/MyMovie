# Python Project - Section A2 Group 1 - MyMovie
##This is the Simple_Regression_Models script. This script contains the functionality of 3 traditional regression methods over different variables.
## Made by Shayne Bement, Jeff Curran, Ghazal Erfani, Naphat Korwanich, and Asvin Sripraiwalsupakit
## Imported by myMovie

import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from math import sqrt

##### %matplotlib qt, if graphs are inline #####

## Linear Regression model with 1 continuous variable and 23 dummy variables
def LinearRegression(df, inputList):

    
    ##### Obtaining Inputs from main #####
    modelInput = inputList
    #[Genre, MPAA, Budget, BookBool, AwardBool]
    
    movieDF = df
    #[Title, Year, Distributor, Genre, MPAA, Budget, Worldwide Gross, Average Rating, BookBool, AwardBool]
    
    ##### Loading the data for the Linear Regression Model #####
    indepMovieDF = pd.DataFrame(movieDF, columns=['Genre', 'MPAA', 'Production_Budget', 'Book_Based', 'award_winning'])
    depMovieDF = pd.DataFrame(movieDF, columns=['Worldwide_Gross'])

    genreDummy = pd.get_dummies(indepMovieDF['Genre'])
    indepMovieDF = indepMovieDF.join(genreDummy)
    indepMovieDF = indepMovieDF.drop(columns=['Genre'])

    mpaaDummy = pd.get_dummies(indepMovieDF['MPAA'])
    indepMovieDF = indepMovieDF.join(mpaaDummy)
    indepMovieDF = indepMovieDF.drop(columns=['MPAA'])
    
    
    ##### Generating the user input DataFrame #####
###print(indepMovieDF.head())
    userInputDF = indepMovieDF[:1]  
    
    for col in userInputDF.columns:
        userInputDF[col].values[:] = 0
    
    userInputDF.at[0, 'Production_Budget'] = modelInput[2]
    userInputDF.at[0, 'Book_Based'] = modelInput[3]
    userInputDF.at[0, 'award_winning'] = modelInput[4]
    userInputDF.at[0, modelInput[0] ] = 1   #Genre
    userInputDF.at[0, modelInput[1] ] = 1   #MPAA
###print(indepMovieDF.head())
    
    ##### Creating Linear Regression Model #####
    ### Generating training data ###
    indepTrain, indepTest = train_test_split(indepMovieDF, test_size=0.25) #set test size?
    depTrain, depTest = train_test_split(depMovieDF, test_size=0.25) #set test size?
    
    ### Training Regression Model ###
    regr = linear_model.LinearRegression()
    regr.fit(indepTrain, depTrain)
    
    depPrediction = regr.predict(indepTest)
    
    ### Calculating RMSE ###
    RMSE = int(sqrt(mean_squared_error(depPrediction, depTest)))

    
    ### Making the prediction with Sample inputs ###
    userInputList = userInputDF.iloc[0,:].tolist()
    predGross = int(regr.predict([userInputList]))

    
    ### Some Discussion on Error ###
# =============================================================================
#     fullDF = depMovieDF.join(indepMovieDF)
#     variables = ['Worldwide_Gross', 'Production_Budget']
#     
#     corr_matrix = fullDF.corr()
#     print(corr_matrix['Worldwide_Gross'].sort_values(ascending=False))
# 
#     pd.plotting.scatter_matrix(fullDF[variables], figsize=(12, 8))
#     plt.show()
# =============================================================================

    return predGross, RMSE
#end LinearRegression
    


## Logistical Regression with 1 continuous variable and 23 dummy variables
def LogisticRegression(df, inputList):
    ##### Obtaining Inputs from main #####
    
    modelInput = inputList
    #[Genre, MPAA, Budget, BookBool, AwardBool]
    
    movieDF = df
    #[Title, Year, Distributor, Genre, MPAA, Budget, Worldwide Gross, Average Rating, BookBool, AwardBool]
    
    
    ##### Loading the data for the Linear Regression Model #####
    indepMovieDF = pd.DataFrame(movieDF, columns=['Genre', 'MPAA', 'Production_Budget', 'Book_Based', 'award_winning'])
    depMovieDF = pd.DataFrame(movieDF, columns=['Worldwide_Gross'])

    genreDummy = pd.get_dummies(indepMovieDF['Genre'])
    indepMovieDF = indepMovieDF.join(genreDummy)
    indepMovieDF = indepMovieDF.drop(columns=['Genre'])

    mpaaDummy = pd.get_dummies(indepMovieDF['MPAA'])
    indepMovieDF = indepMovieDF.join(mpaaDummy)
    indepMovieDF = indepMovieDF.drop(columns=['MPAA'])
    
    
    ##### Generating the user input DataFrame #####
    userInputDF = indepMovieDF[:1]
    
    for col in userInputDF.columns:
        userInputDF[col].values[:] = 0
    
    userInputDF.at[0, 'Production_Budget'] = modelInput[2]
    userInputDF.at[0, 'Book_Based'] = modelInput[3]
    userInputDF.at[0, 'award_winning'] = modelInput[4]
    userInputDF.at[0, modelInput[0] ] = 1   #Genre
    userInputDF.at[0, modelInput[1] ] = 1   #MPAA
 
    
    ##### Creating Linear Regression Model #####
    ### Generating training data ###
    indepTrain, indepTest = train_test_split(indepMovieDF, test_size=0.25) #set test size?
    depTrain, depTest = train_test_split(depMovieDF, test_size=0.25) #set test size?
   
    ### Training Regression Model ###
    logReg = linear_model.LogisticRegression()
    logReg.fit(indepTrain, depTrain.values.ravel())
    
    depPrediction = logReg.predict(indepTest)
    
    ### Calculating RMSE ###
    RMSE = int(sqrt(mean_squared_error(depPrediction, depTest)))

    
    ### Making the prediction with Sample inputs ###
    userInputList = userInputDF.iloc[0,:].tolist()
    predGross = int(logReg.predict([userInputList]))
  
    
    ### Some Discussion on Error ###
# =============================================================================
#     fullDF = depMovieDF.join(indepMovieDF)
#     variables = ['Worldwide_Gross', 'Production_Budget']
#     
#     corr_matrix = fullDF.corr()
#     print(corr_matrix['Worldwide_Gross'].sort_values(ascending=False))
# 
#     pd.plotting.scatter_matrix(fullDF[variables], figsize=(12, 8))
#     plt.show()
# =============================================================================

    return predGross, RMSE
#end LogisticRegression


## Simplified Linear Regression model with 1 continuous variable
def BudgetOnlyRegression(df, inputList):
     ##### Obtaining Inputs from main #####
    
    modelInput = inputList[2]
    #[Genre, MPAA, Budget, BookBool, AwardBool]
    
    movieDF = df
    #[Title, Year, Distributor, Genre, MPAA, Budget, Worldwide Gross, Average Rating, BookBool, AwardBool]
    
    
    ##### Loading the data for the Linear Regression Model #####
    budgetDF = pd.DataFrame(movieDF, columns=['Production_Budget'])
    depMovieDF = pd.DataFrame(movieDF, columns=['Worldwide_Gross'])

    ##### Generating the user input DataFrame #####
    userInputDF = budgetDF[:1]
    
    for col in userInputDF.columns:
        userInputDF[col].values[:] = 0
    userInputDF.at[0, 'Production_Budget'] = modelInput
    
    ##### Creating Linear Regression Model #####
    ### Generating training data ###
    budgetTrain, budgetTest = train_test_split(budgetDF, test_size=0.25) #set test size?
    depTrain, depTest = train_test_split(depMovieDF, test_size=0.25) #set test size?
    
    ### Training Regression Model ###
    budgetRegr = linear_model.LinearRegression()
    budgetRegr.fit(budgetTrain, depTrain)
    
    budgetPrediction = budgetRegr.predict(budgetTest)
    
    ### Calculating RMSE ###
    RMSE = int(sqrt(mean_squared_error(budgetPrediction, budgetTest)))
    
    ### Making the prediction with Sample inputs ###
    userInputList = userInputDF.iloc[0,:].tolist()
    predGross = int(budgetRegr.predict([userInputList]))
    
    ### Some Discussion on Error ###
# =============================================================================
#     fullDF = depMovieDF.join(budgetDF)
#     variables = ['Worldwide_Gross', 'Production_Budget']
#     
#     corr_matrix = fullDF.corr()
#     print(corr_matrix['Worldwide_Gross'].sort_values(ascending=False))
# 
#     pd.plotting.scatter_matrix(fullDF[variables], figsize=(12, 8))
#     plt.show()
# =============================================================================

    return predGross, RMSE
#end BudgetOnlyRegression



##if testing the script individually this will run.
if __name__ == "__main__":
    modelInput = ['Comedy', 'PG-13', 50000000, 1, 0]
    movieDF = pd.read_csv(r'FullOutput.csv')
    
    grossEarnings, errorTerm = LinearRegression(movieDF, modelInput)
    logGrossEarnings, logErrorTerm = LogisticRegression(movieDF, modelInput)
    budgetEarnings, budgetErrorTerm = BudgetOnlyRegression(movieDF, modelInput)
    
    
    print('\n\033[4mLinear Regression Model\033[0m')
    print('Projected Budget: ', "${:,}".format(modelInput[2]))
    print('Predicted Gross Budget: ', "${:,}".format(grossEarnings))
    print('predicted Root Mean Squared Error: ', "${:,}".format(errorTerm))
    
    print('\n\033[4mLinear Regression Model (Budget Only)\033[0m')
    print('Projected Budget: ', "${:,}".format(modelInput[2]))
    print('Predicted Budget Gross Budget: ', "${:,}".format(budgetEarnings))
    print('predicted Budget Root Mean Squared Error: ', "${:,}".format(budgetErrorTerm))
    
    print('\n\033[4mLogistic Regression Model\033[0m')
    print('Projected Budget: ', "${:,}".format(modelInput[2]))
    print('Predicted Gross Budget: ', "${:,}".format(logGrossEarnings))
    print('predicted Root Mean Squared Error: ', "${:,}".format(logErrorTerm))
