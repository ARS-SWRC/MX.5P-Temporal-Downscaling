from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from statsmodels.tools import categorical
import pandas as pd
import numpy as np
from pathlib import Path


###############################################################################
'USER INPUT'
'work_directory: folder path string to input files'
'input_file options: MX5P_XY_Zmin.csv string where Z is 60, 180 or 1440'
'resolution options: 60, 180 or 1440'
'model options: RF or GB strings'
'user_file: file string from user with predictor variables'
'user_file placeholders use original X data.'
'*file paths for windows OS.'
###############################################################################
working_directory = Path('output')
fitting_file = 'MX5P_XY_60min.csv' 
user_file = 'MX5P_X_60min_Placeholder.csv'
resolution = 60 
model = 'GB'
###############################################################################



###############################################################################
'fitting data'
###############################################################################
par_dict = {'RF60':[50, 20, 200], 'RF180':[50, 20, 200], 'RF1440':[100, 20, 200],
            'GB60':[400, 2, 5], 'GB180':[400, 2, 5], 'GB1440':[400, 2, 5] }

pars = par_dict[model + str(resolution)]

file_df = pd.read_csv(fitting_file, header=0)

X = file_df.loc[:,'MX.5P_up':]
y = file_df['MX.5P_brkpt']

month_labels = ['mo-' + str(item) for item in list(sorted(file_df['Month'].unique()))]
month_list = np.array(file_df['Month'].tolist())
month_cat = categorical(month_list, drop=True)

columns = list(X.columns)
columns.extend(month_labels)

X_cat = np.concatenate((X, month_cat), axis=1)
X = pd.DataFrame(X_cat, columns=columns)



###############################################################################
'prediction data'
###############################################################################
user_df = pd.read_csv(user_file, header=0)

X_user = user_df.loc[:,:]

month_labels_user = ['mo-' + str(item) for item in list(sorted(user_df['Month'].unique()))]
month_list_user = np.array(user_df['Month'].tolist())
month_cat_user = categorical(month_list_user, drop=True)

columns_user = list(X_user.columns)
columns_user.extend(month_labels_user)

X_cat_user = np.concatenate((X_user, month_cat_user), axis=1)
X_user = pd.DataFrame(X_cat_user, columns=columns_user)



###############################################################################
'model fitting'
###############################################################################
regr = eval('RandomForestRegressor' if model == 'RF' else 'GradientBoostingRegressor')(
        n_estimators=pars[0], 
        max_depth=pars[1], 
        max_leaf_nodes=pars[2], 
        min_samples_split=20,
        min_samples_leaf=20, 
        max_features='log2', 
        random_state=123)

regr.fit(X, y)



###############################################################################
'predicting'
###############################################################################
y_pred = regr.predict(X_user)
        


###############################################################################
'writing predictions to file'
###############################################################################

if not working_directory.exists():
    working_directory.mkdir(parents=True, exist_ok=True)

with open(working_directory / 'out.txt', 'w') as f:
    
    for value in y_pred:
        
        f.write(str(value) + '\n')

    
