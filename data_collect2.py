# import code; code.interact(local=locals())
from __future__ import division
import csv
import matplotlib.pyplot as plt

#ag_im refers to agricultural imports as percent of merchandise imports
ag_im = []
with open('ag_import3.csv', 'rU') as file:
    data = csv.DictReader(file)
    for row in data:
        ag_im.append(row)

countries = []
for r in ag_im:
    countries.append(r['Country Name'])

years = range(1962,2014)

country_data = {}
for c in countries:
    for r in ag_im:
        if r['Country Name'] == c :
            data=[]
            for y in years:
                data.append(r[str(y)])
            country_data[c] = data

processed_country_data = {}


data = country_data['Drewtopia']
print data

processed_country_data = {}

for c in country_data:
    data = country_data[c]
    #convert empty strings to zeros
    counter = 0
    for d in data:
        if d == '':
            data[counter] = 0
        else:
            data[counter] = float(d)
        counter += 1
    #trim zeros
    trim_zeros = []
    counter = 0
    for d in data:
        if d == 0:
            d = d
        else:
            trim_zeros.append(d)
        counter += 1
    if len(trim_zeros)>0:
        ave = sum(trim_zeros)/float(len(trim_zeros)) #if L else '-'
        low = min(trim_zeros)
        high = max(trim_zeros)
        diff = high - low

        c_data = {}
        c_data['average'] = ave
        c_data['maximum'] = high
        c_data['minimum'] = low
        c_data['difference'] = diff
        c_data['data'] = data
        processed_country_data[c] = c_data

print processed_country_data['Drewtopia']
