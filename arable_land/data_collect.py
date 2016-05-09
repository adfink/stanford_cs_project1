# import code; code.interact(local=locals())
from __future__ import division
import csv
import matplotlib.pyplot as plt

class DataParser:
    'reads in CSV and does things with it'


    def __init__(self, file_name,):
        self.file_name = file_name
        self.years = range(1962,2014)


    def process_data(self):
        #take in data from CSV as a list of dictionaries
        raw_data = []
        with open(self.file_name, 'rU') as file:
            data = csv.DictReader(file)
            for row in data:
                raw_data.append(row)
        #compile a list of all the countries
        countries = []
        for r in raw_data:
            countries.append(r['Country Name'])

        country_data = {}
        for c in countries:
            for r in raw_data:
                if r['Country Name'] == c :
                    data=[]
                    for y in self.years:
                        data.append(r[str(y)])
                    country_data[c] = data


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
        averages = []
        differences = []
        for c in processed_country_data:
            av = processed_country_data[c]['average']
            diff = processed_country_data[c]['difference']
            averages.append(av)
            differences.append(diff)
        averages.sort()
        differences.sort()
        lower_limit = averages[4]
        upper_limit = averages[len(averages)-5]
        most_diff = differences[len(averages)-5]
        least_diff = differences[4]

        high_av_counties = []
        low_av_counties = []
        high_variable_countries = []
        low_variable_countries = []
        for c in processed_country_data:
            if processed_country_data[c]['average'] >= upper_limit:
                high_av_counties.append(c)
            if processed_country_data[c]['average'] <= lower_limit:
                low_av_counties.append(c)
            if processed_country_data[c]['difference'] >= most_diff:
                high_variable_countries.append(c)
            if processed_country_data[c]['difference'] <= least_diff:
                low_variable_countries.append(c)

        #fill in zero values with average
        for c in processed_country_data:
            counter = 0
            for d in processed_country_data[c]['data']:
                if d == 0:
                    processed_country_data[c]['data'][counter] = processed_country_data[c]['average']
                counter += 1

        self.raw_data = raw_data
        self.countries = countries
        self.country_data = country_data
        self.processed_country_data = processed_country_data
        self.high_av_counties = high_av_counties
        self.low_av_counties = low_av_counties
        self.high_variable_countries = high_variable_countries
        self.graph_able_data = []
        self.graph_able_data.append(high_av_counties)
        self.graph_able_data.append(low_av_counties)
        self.graph_able_data.append(high_variable_countries)
        self.graph_able_data.append(low_variable_countries)

    def graph_data(self, data_id):
        color = ['blue','green','yellow','red','orange']
        counter = 0
        plt.figure()
        for c in self.graph_able_data[data_id]:
            x = self.processed_country_data[c]['data']
            y = self.years
            plt.plot(y,x,color=color[counter])
            counter += 1
        # x = self.processed_country_data['United States']['data']
        # y = self.years
        # plt.plot(y,x,color='black')


        plt.legend(self.graph_able_data[data_id])
        plt.show()




minion = DataParser('arable_land.csv')
minion.process_data()
minion.graph_data(3)
