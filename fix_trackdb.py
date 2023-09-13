import sys
import pandas as pd


"""
Script to correct the bug from trackhub package to print the priority field
"""

f_track = sys.argv[1] #trackDB.txt file generate by trackhub script
df = pd.read_csv(sys.argv[2]) #names_trackhub.csv file to get the priority info

dict_p = dict(zip(df['final_name'], df['order'])) #get priority order


for line in open(f_track).readlines():
    print(line, end="")
    if line.startswith("track"):
        name = line.strip().split(' ')[1]
        # print(name)
        print('priority',dict_p.get(name))

