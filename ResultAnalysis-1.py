# Divyansh Purohit
# 101903438
# 3COE17

import sys
import pandas as pd
import numpy as np
import logging
import warnings
import os
from itertools import chain
warnings.filterwarnings("ignore")

logging.basicConfig(filename='101903438-log.txt', level=logging.DEBUG, format="%(message)s")


logging.info("________________________________________________\nScript Running Errors are logged below:")
if(len(sys.argv) != 2):
    log_msg = '2 parameter expected (including script name), found {}.\nCorrect Input format -> python 101903438-1.py input.csv'.format(len(sys.argv))
    logging.error(log_msg)
    raise Exception(log_msg)

file = []
for (root,dirs,files) in os.walk('.'):
    file.append(files)
    

file = list(chain.from_iterable(file))

if(sys.argv[1] not in file):
    err_msg = 'No file with that name ({}) found in the current directory. Please correct the input and try again'.format(sys.argv[1])
    logging.error(err_msg)
    raise Exception(err_msg)

input_file_name = './' + sys.argv[1]
df = pd.read_csv(input_file_name)

if(df.shape[1] != 3):
    err_msg = "Invalid format of input csv file. 3 columns expected, found {}".format(df.shape[1])
    logging.error(err_msg)
    raise Exception(err_msg)

logging.warning("\n")
logging.warning("The following students marks have not been recorded:")
logging.info('Roll Number\t\tSubmission\t\tMarks')
for index in range(len(df)):
     if(df['Marks'][index] in ('X','-','','NAN','NaN','nan',' ',np.NaN) ):
         logging.info('{} \t\t {} \t\t {}'.format(df['RollNumber'][index], df['Submission'][index], df['Marks'][index]))
         df['Marks'][index] = 0


subjects = df['Submission'].unique()
stu = df['RollNumber'].unique()
output=df
for sub in subjects:
    output[sub] = 0


for index in output.index:
    for sub in subjects:
        output[sub][index] = output['Marks'][index] if output['Submission'][index] == sub else 0
 
 
output.drop(['Submission', 'Marks'], axis=1, inplace=True)

for index in range(len(output.index)):
    for j in range(index+1, len(output.index)):
        if output['RollNumber'][index] == output['RollNumber'][j]:
            for sub in subjects:    
                output[sub][index] = output[sub][j] if output[sub][index] == 0 else output[sub][index]
                
output = output.drop_duplicates(subset=['RollNumber'])

output.reset_index(inplace=True)
output.drop(['index'], axis=1, inplace=True)

output.to_csv('./101903438-output.csv', index=False)
