#import numpy as np
#import time
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score

from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
#from sklearn.ensemble import BaggingClassifier
import pickle

import sqlite3 
#=======================================================================
conn = sqlite3.connect('D:/Alka_python_2019_20/Alka_python_2019_20/Credit_Card/creditcarddb.db')


Sqlstr = "SELECT T.TCCNo,C.Id,T.TMMName,T.TMMState,T.Trans_Amt,T.TM_Status FROM Tamp_master T, card_master C WHERE T.TCCNo=C.cardno order by C.Id,T.TM_Status;"

#=======================================================================
#--------------------------------------------------------------------
df = pd.read_sql_query(Sqlstr, conn)
#print(df.head(10))


df_new=df.drop(['TCCNo'], axis=1)

df_new['TMMName'] = df['TMMName'].astype(int)
df_new['TMMState'] = df['TMMState'].astype(int)

df_new['id'] = df['id'].astype(int)
df_new['TM_Status'] = df_new['TM_Status'].astype(int)


df_new.sort_values(by=['id','TM_Status'],ascending=True,inplace=True)
#sort_by_life = gapminder.sort_values('lifeExp')
#df_new=df_new.sort_values(by=0,ascending=True,inplace=True)
#df_new.head(203)
#------------------------------------------------------------------------------

features = list(df_new[['id','TMMName','TMMState','Trans_Amt']])
target = list(df_new[['TM_Status']])


X = df_new[features] #our features that we will use to predict Y
Y = df_new[target]

#--------------------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.3, random_state=4)
#--------------------------------------------------------------------------------------

##########################################==================================================
####SVM Classifier#################
def SVM_Cl():
    C = 1.0
    
    
    clf_SVM = svm.SVC(kernel='linear',C=C)
    #prediction = clf_SVM.predict(X)
    
    clf_SVM .fit(X_train, y_train.values.ravel()) 
    prediction =clf_SVM.predict(X_test)
    
    
    
    ## now you can save it to a file
    with open('clf_SVM.pkl', 'wb') as f:
        pickle.dump(clf_SVM, f)
        
#    print("SVM Accuracy: {0:.2%}".format(accuracy_score(prediction, y_test.values.ravel())))
#    print("Execution time: {0:.5} seconds \n".format(end-start))
    
    A="SVM Accuracy: {0:.2%}".format(accuracy_score(prediction, y_test.values.ravel()))
    C="SVM Model Saved as <<  clf_SVM.pkl  >>"
    D=A+'\n'+ C
    
    return D
#
## and later you can load it
#with open('clf_SVM.pkl', 'rb') as f:
#    clf_SVM = pickle.load(f)
#
#Predict_to_value=np.array([1,15,1,1000])
#Predict_to_value=Predict_to_value.reshape(1, -1)
#Predict_get_value=clf_SVM.predict(Predict_to_value)
#print(Predict_get_value)



#-------------------------------------------------------------------------------------------------
def DST_Cl():   
    
    clf_gini = DecisionTreeClassifier(criterion = "gini",random_state = 100,max_depth=3, min_samples_leaf=5) 
    
    
    clf_gini.fit(X_train, y_train.values.ravel()) 
    
    
    prediction = clf_gini.predict(X_test)
    #scores = cross_val_score(clf_gini, X,Y.values.ravel(), cv=5)
    
       ## now you can save it to a file
    with open('clf_DST.pkl', 'wb') as f:
        pickle.dump(clf_gini, f)

    A="Decision Tree Accuracy: {0:.2%}".format(accuracy_score(prediction, y_test.values.ravel()))
    C="Decision Tree Model Saved as <<  clf_DST.pkl  >>"

    D = A+'\n'+ C
    
    return D
##----------------------------------------------------------------------------------------------------
#
def NB_Cl():
    
    clf_Naive = GaussianNB()
    clf_Naive.fit(X_train, y_train.values.ravel())
    
    prediction = clf_Naive.predict(X_test)
    #scores = cross_val_score(clf_Naive, X,Y.values.ravel(), cv=5)
       
    #Predict_to_value=np.array([83.91,29,222.87])
    #Predict_to_value=Predict_to_value.reshape(1, -1)
    #Predict_get_value=clf_Naive.predict(Predict_to_value)
    #print(Predict_get_value)
           ## now you can save it to a file
    with open('clf_NB.pkl', 'wb') as f:
        pickle.dump(clf_Naive, f)

    
    A="Naive Bayes Accuracy: {0:.2%}".format(accuracy_score(prediction, y_test.values.ravel()))
    C="Naive Bayes Model Saved as <<  clf_NB.pkl  >>"

    D = A+'\n'+ C
    return D

#####CNN Model ################################################
#from keras.models import Sequential
#from keras.layers.convolutional import Conv1D
#from keras.layers import MaxPooling1D
#from keras.layers import Flatten
#from keras.layers import Dense
#from keras.callbacks import ModelCheckpoint
## define model
#
#model = Sequential()
#
#model.add(Dense(output_dim = 8, init = 'uniform', activation = 'relu', input_dim =4))
#model.add(Dense(output_dim = 16, init = 'uniform', activation = 'relu'))
#model.add(Dense(output_dim = 8, init = 'uniform', activation = 'relu'))
#
#model.add(Dense(output_dim = 1, init = 'uniform', activation = 'sigmoid'))
#
#model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
#
#checkpointer2 = ModelCheckpoint(filepath='weights.hdf5', verbose=1, save_best_only=True)
#model.summary()
#model.fit(X_train, y_train, batch_size=32, epochs=50,validation_data=(X_test, y_test), callbacks=[checkpointer2])

# fit model
#######################DATA GENRATER##############################

##-----------------------------------------------------------------------------------------------------------
#
##df_new=df.loc[(df['ADMISSION'] ==0)& (df['Age'] ==29)]
##df_new
##
###--------------------------------------------------------------------------------------------------------
##ndf=df.groupby(df['D_Internet_Usage'])
##ndf.first() 
###----------------------------------------------------------------------------------------------------
##df_new=df.loc[(df['D_Internet_Usage'] >=df['D_Time_Site'].max())]
##df_new
###---------------------------------------------------------------------------------------------------
##df_new=df.loc[(df['Age'] >=40)]
##df_new
##===========================================================================================
#c.close()
conn.close()

#============================================================================================