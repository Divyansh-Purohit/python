# Divyansh Purohit
# 101903438
# 3COE17

import sys
import matplotlib.pyplot as plt
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
    log_msg = '2 parameter expected (including script name), found {}.\nCorrect Input format -> python 101903438-2.py input.csv'.format(len(sys.argv))
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
df2 = pd.read_csv(input_file_name, na_values=[0])

if(df.shape[1] != 6):
    err_msg = "Invalid format of input csv file. 6 columns expected, found {}".format(df.shape[1])
    logging.error(err_msg)
    raise Exception(err_msg)
logging.warning("\n")
subjects = df.columns
subjects = subjects[1:]
df.index = df['RollNumber']
df.drop(['RollNumber'], axis=1, inplace=True)
df = df.T

# Histograms
for i in df.columns:
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    ax1.hist(df[i], bins=50)
    ax1.set_xlabel('Marks (in different subjects)')
    ax1.set_ylabel('No. of subjects')
    ax1.set_title('Histogram of RollNumber {}'.format(i))
    fig.savefig(fname='./{}-Histogram'.format(i), pad_inches = 1, facecolor='w', edgecolor='g')
    

# Line Charts
for i in df.columns:
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    ax1.plot(df[i])
    ax1.set_xlabel('Marks (in different subjects)')
    ax1.set_ylabel('No. of subjects')
    ax1.set_title('Line Chart of RollNumber {}'.format(i))
    fig.savefig(fname='./{}-Line Chart'.format(i), pad_inches = 1, facecolor='w', edgecolor='g')
    
# Pie Charts
for i in df.columns:
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    ax1.pie(df[i], labels=subjects)
    ax1.set_ylabel('% of marks obtained')
    ax1.set_title('Pie Chart of RollNumber {}'.format(i))
    fig.savefig(fname='./{}-Pie Chart'.format(i), pad_inches = 1, facecolor='w', edgecolor='g')
# writing to file
output_fname = '101903438-statistics.txt'
fname = open(output_fname, 'w')
fname.write('Missing/Non Numerical and Zero Values are not considered for calculating min, max, median, mean, standard dev, otherwise they would badly affect these calculations.\n\n')
# caclulating statistics about individual subjects
total_nonmissing=np.array([])
total_missing = 0
i=0
for sub in subjects:
    fname.write('Maximum marks in subject {} are: {}\n'.format(sub, df2[sub].max()))
    fname.write('Minimum marks in subject {} are: {}\n'.format(sub, df2[sub].min()))
    fname.write('Mean marks in subject {} are: {}\n'.format(sub, round(df2[sub].mean(),2)))
    fname.write('Median marks in subject {} is: {}\n'.format(sub, df2[sub].median()))
    fname.write('Standard Deviation of marks in subject {} is: {}\n'.format(sub, round(df2[sub].std(),2)))
    total_missing += df2[sub].isnull().sum()
    total_nonmissing = np.append(total_nonmissing, df2.shape[0]-df2[sub].isnull().sum())
    fname.write('Number of missing values in subject {} are: {} \n'.format(sub, df2[sub].isnull().sum()))
    fname.write('Number of non numreic values in subject {} are: 0 (Since the dataframe has already been processed in question-1, all non numeric values have been converted to 0)\n\n'.format(sub))    
fname.write('Total number of missing values in the entire dataframe are:{}\n'.format(total_missing))
fname.write('Total non numreic values are: 0 (Since the dataframe has already been processed in question-1, all non numeric values have been converted to 0)\n\n\n')
# calculating overall statistics of the input data
sum_all_values = df2[subjects].sum().sum()
total_non_missing = np.sum(total_nonmissing)
mean_marks = round(sum_all_values/total_non_missing, 3)
median_all_data = round(df2.median().median(),3)
standard_dev_all_data = round(df2[subjects].std().std(),3)
# writing to file overall statictics
fname.write("Total marks in all subjects: {}\n".format(sum_all_values))
fname.write("Mean marks of all subjects: {}\n".format(mean_marks))
fname.write("Median marks of all subjects: {}\n".format(median_all_data))
fname.write("Standard Deviation of marks of all subjects: {}\n".format(standard_dev_all_data))
# closing the file
fname.close()
# generating individual statistics
df2['Sum'] = df2[subjects].sum(axis=1)
df2['Mean'] = df2['Sum']/len(subjects)
df2['Median'] = df2[subjects].median(axis=1, skipna=True)
df2['STD'] = round(df2[subjects].std(axis=1),2)
df2['Max'] = df2[subjects].max(axis=1, skipna=True)
df2['Min'] = df2[subjects].min(axis=1, skipna=True)

for index in df2.index[0:5]:
    fout=  '{}-statistics.txt'.format(df2['RollNumber'][index])
    with open(fout, 'w') as fa:
        fa.write('Statistics of RollNumber {} are given below:\n\n'.format(df2['RollNumber'][index]))
        fa.write('Total marks scored in all subjects are: \n'.format(df2['Sum'][index]))
        fa.write('Mean marks are: \n'.format(df2['Mean'][index]))
        fa.write('Median marks are: \n'.format(df2['Median'][index]))
        fa.write('Standard deviation of marks are: \n'.format(df2['STD'][index]))
        fa.write('Maximum marks scored are: \n'.format(df2['Max'][index]))
        fa.write('Minimum marks scored are: \n'.format(df2['Min'][index]))
        fa.flush()
        fa.close()