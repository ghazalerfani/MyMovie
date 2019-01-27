## Python Project - Section A2 Group 1 - MyMovie
## This is KNN_DecisionTree_Regressions. This contains the functions for working through the KKN and Decision tree regressions.
## Made by Shayne Bement, Jeff Curran, Ghazal Erfani, Naphat Korwanich, and Asvin Sripraiwalsupakit
## Imported by myMovie

import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn import tree
from math import sqrt
from sklearn.metrics import mean_squared_error 
from sklearn.neighbors import KNeighborsClassifier
import warnings

## using k-nearest neighbors algorithm to classify user-inputted values into 1 of 10 ranges of world-wide gross values 
def KNN_Regression(df, inputList):
    ### in case grader sklearn is not updated to most recent version, this will
    ### remove a depreciated warning regarding numpy
    warnings.filterwarnings(action='ignore', category=DeprecationWarning)
    
    ## Putting data required for model into pandas dataframe  
    df = pd.DataFrame(df, columns=['Genre', 'MPAA', 'Production_Budget', 'Book_Based', 'award_winning', 'Worldwide_Gross'])
    
    ### Obtaining Inputs from main
    modelInput = inputList
    #[Genre, MPAA, Budget, BookBool, AwardBool]

    ## Converting categorical variables 
    dfgenre = pd.get_dummies(df['Genre'], drop_first=True)
    df = df.join(dfgenre)
    df = df.drop(columns=['Genre'])

    dfmpaa = pd.get_dummies(df['MPAA'])
    df = df.join(dfmpaa)
    df = df.drop(columns=['MPAA'])

    ## Creating categorical variable to be predicted
    df['Production_Budget'] = df['Production_Budget'].astype('int')
    df['Worldwide_Gross'] = df['Worldwide_Gross'].astype('int')
    le5 = preprocessing.LabelEncoder()
    conditions = [
     (df['Worldwide_Gross'] <= 1000000),
     (df['Worldwide_Gross'] > 1000000) & (df['Worldwide_Gross'] <= 5000000),
     (df['Worldwide_Gross'] > 5000000) & (df['Worldwide_Gross'] <= 25000000),
     (df['Worldwide_Gross'] > 25000000) & (df['Worldwide_Gross'] <= 50000000),
     (df['Worldwide_Gross'] > 50000000) & (df['Worldwide_Gross'] <= 250000000),
     (df['Worldwide_Gross'] > 250000000) & (df['Worldwide_Gross'] <= 500000000),
     (df['Worldwide_Gross'] > 500000000) & (df['Worldwide_Gross'] <= 1000000000),    
     (df['Worldwide_Gross'] > 1000000000) & (df['Worldwide_Gross'] <= 1500000000), 
     (df['Worldwide_Gross'] > 1500000000) & (df['Worldwide_Gross'] <= 2000000000),
     (df['Worldwide_Gross'] > 2000000000)]
    choices = ['0 - 1,000,000', '1,000,000 - 5,000,000','5,000,000 - 25,000,000','25,000,000 - 50,000,000','50,000,000 - 250,000,000','250,000,000 - 500,000,000','500,000,000 - 1,000,000,000','1,000,000,000 - 1,500,000,000','1,500,000,000 - 2,000,000,000','> 2,000,000,000']
    df['Worldwide_Gross'] = np.select(conditions, choices, default='0 - 1,000,000')    
    df['Worldwide_Gross'] = le5.fit_transform(df['Worldwide_Gross'])

    ## Generating user input dataframe
    df1 = df.drop(columns=['Worldwide_Gross'])
    userinputdf = df1[:1]
    for col in userinputdf.columns:
        userinputdf[col].values[:] = 0
            
    userinputdf.at[0, 'Production_Budget'] = modelInput[2]
    userinputdf.at[0, 'Book_Based'] = modelInput[3]
    userinputdf.at[0, 'award_winning'] = modelInput[4]
    userinputdf.at[0, modelInput[0] ] = 1   #Genre
    userinputdf.at[0, modelInput[1] ] = 1   #MPAA

    ## Creating train and test data set
    train , test = train_test_split(df, test_size = 0.3)
    x_train = train.drop('Worldwide_Gross', axis=1)
    y_train = train['Worldwide_Gross']
    x_test = test.drop('Worldwide_Gross', axis = 1)
    y_test = test['Worldwide_Gross']

    ## Calculating RMSE
    model = KNeighborsClassifier(n_neighbors=10)
    model.fit(x_train, y_train) 
    pred=model.predict(x_test)
    rmse = int(sqrt(mean_squared_error(y_test,pred)))

    ## Making the prediction with inputs
    userInputList = userinputdf.iloc[0,:].tolist()
    predicted = int(model.predict([userInputList])) 
    predicted = str(le5.inverse_transform(predicted))
    
    return predicted, rmse

## using decision tree regression model to predict a worldwide gross using sequences of branching operations based on comparisons of the variables
def DecisionTree_Regression(df, inputList):
    ## Putting data required for model into pandas dataframe  
    df = pd.DataFrame(df, columns=['Genre', 'MPAA', 'Production_Budget', 'Book_Based', 'award_winning', 'Worldwide_Gross'])
    
    ### Obtaining Inputs from main 
    modelInput = inputList
    #[Genre, MPAA, Budget, BookBool, AwardBool]

    ## Converting categorical variables to dummy variables
    dfgenre = pd.get_dummies(df['Genre'], drop_first=True)
    df = df.join(dfgenre)
    df = df.drop(columns=['Genre'])

    dfmpaa = pd.get_dummies(df['MPAA'])
    df = df.join(dfmpaa)
    df = df.drop(columns=['MPAA'])

    ## Generating user input dataframe for prediction
    df1 = df.drop(columns=['Worldwide_Gross'])
    
    userinputdf = df1[:1]
    for col in userinputdf.columns:
        userinputdf[col].values[:] = 0
            
    userinputdf.at[0, 'Production_Budget'] = modelInput[2]
    userinputdf.at[0, 'Book_Based'] = modelInput[3]
    userinputdf.at[0, 'award_winning'] = modelInput[4]
    userinputdf.at[0, modelInput[0] ] = 1   #Genre
    userinputdf.at[0, modelInput[1] ] = 1   #MPAA

    ## Creating train and test data set
    train , test = train_test_split(df, test_size = 0.3)
    x_train = train.drop('Worldwide_Gross', axis=1)
    y_train = train['Worldwide_Gross']
    x_test = test.drop('Worldwide_Gross', axis = 1)
    y_test = test['Worldwide_Gross']

    ## Calculateing Model RMSE
    model = tree.DecisionTreeRegressor()
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    rmse = int(sqrt(mean_squared_error(y_test,pred)))

    ## Making the prediction with inputs
    userInputList = userinputdf.iloc[0,:].tolist()
    predicted = int(model.predict([userInputList]))

    ## Some discussion on error
    # variables = ['Worldwide_Gross', 'Production_Budget']

    # corr_matrix = df.corr()
    # print(corr_matrix['WWorldwide_Gross'].sort_values(ascending=False))

    # pd.scatter_matrix(df[variables], figsize=(12, 8))
    # plt.show()

    return predicted, rmse


if __name__ == "__main__":
####### Start #########
    modelInput = ['Comedy', 'PG-13', 50000000, 1, 0]
    movieDF = pd.read_csv(r'FullOutput.csv')
    
    grossEarningsRange, errorTerm = KNN_Regression(movieDF, modelInput)
    grossEarnings, errorTerm = DecisionTree_Regression(movieDF, modelInput)
    
    print('\n\033[4mKNN Regression Model\033[0m')
    print('Projected Budget: ', "${:,}".format(modelInput[2]))
    print('Predicted Gross Budget: ', "${}".format(grossEarningsRange))
    print('predicted Root Mean Squared Error: ', "{:,}".format(errorTerm))
    
    print('\n\033[4mDecision Tree Model\033[0m')
    print('Projected Budget: ', "${:,}".format(modelInput[2]))
    print('Predicted Budget Gross Budget: ', "${:,}".format(grossEarnings))
    print('predicted Budget Root Mean Squared Error: ', "${:,}".format(errorTerm))
   

