# import code; code.interact(local=locals())
from __future__ import division
import csv
import matplotlib.pyplot as plt

class DataParser:
    'reads in CSV and does things with it'

    def __init__(self, file_name,):
        self.file_name = file_name
        self.years = range(1962,2014)
        ########################################################################################
        self.title_name = "Food Production Index (2004-2006 = 100)"
        self.y_axis = "index"
        ########################################################################################
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
                for n in trim_zeros:
                    st_de = []
                    x = (n - ave)*(n - ave)
                    st_de.append(x)
                sd_ave = sum(st_de)/float(len(st_de))
                sd = sd_ave ** (0.5)

                c_data = {}
                c_data['average'] = ave
                c_data['maximum'] = high
                c_data['minimum'] = low
                c_data['difference'] = diff
                c_data['stan_dev'] = sd
                c_data['data'] = data
                processed_country_data[c] = c_data
        averages = []
        differences = []
        standard_devi = []
        for c in processed_country_data:
            av = processed_country_data[c]['average']
            diff = processed_country_data[c]['difference']
            stan_de = processed_country_data[c]['stan_dev']
            averages.append(av)
            differences.append(diff)
            standard_devi.append(stan_de)
        averages.sort()
        differences.sort()
        standard_devi.sort()

        lower_limit = averages[4]
        upper_limit = averages[len(averages)-5]
        most_diff = differences[len(averages)-5]
        least_diff = differences[4]
        most_standard_devi = standard_devi[len(standard_devi)-5]
        least_standard_devi = standard_devi[4]


        high_av_counties = []
        low_av_counties = []
        high_variable_countries = []
        low_variable_countries = []
        relative_high_variable_countries = []
        relative_low_variable_countries = []
        for c in processed_country_data:
            if processed_country_data[c]['average'] >= upper_limit:
                high_av_counties.append(c)
            if processed_country_data[c]['average'] <= lower_limit:
                low_av_counties.append(c)
            if processed_country_data[c]['difference'] >= most_diff:
                high_variable_countries.append(c)
            if processed_country_data[c]['difference'] <= least_diff:
                low_variable_countries.append(c)
            if processed_country_data[c]['stan_dev'] <= least_standard_devi:
                relative_low_variable_countries.append(c)
            if processed_country_data[c]['stan_dev'] >= most_standard_devi:
                relative_high_variable_countries.append(c)

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
        self.graph_able_data.append(relative_low_variable_countries)
        self.graph_able_data.append(relative_high_variable_countries)
        self.data_sets = ['Five countries with highest {}'.format(self.title_name),
                          "Five countries with the lowest {}".format(self.title_name),
                          "Five countries with the most variability in the {}".format(self.title_name),
                          "Five countries with the lowest variability in the {}".format(self.title_name),
                          "Five countries with the lowest standard deviation in the {}".format(self.title_name),
                          "Five countries with the highest standard deviation in the {}".format(self.title_name)]

    def graph_data(self, data_id):
        color = ['blue','green','yellow','red','orange']
        counter = 0
        plt.figure()
        for c in self.graph_able_data[data_id]:
            x = self.processed_country_data[c]['data']
            y = self.years
            plt.plot(y,x)
            plt.suptitle(self.data_sets[data_id], fontsize=20)
            plt.ylabel(self.y_axis, fontsize=18)
            plt.xlabel('years', fontsize=16)
            counter += 1
            # import code; code.interact(local=locals())
        # use this code if you want to include where the united states falls on the chart
        # x = self.processed_country_data['United States']['data']
        # y = self.years
        # plt.plot(y,x,color='black')
        plt.legend(self.graph_able_data[data_id])
        plt.show()



###################################################################################################
# minion1 = DataParser('arable_land.csv')
# minion2 = DataParser('ag_machinery_per_km_arable_land.csv')
# ag_irrigated_land_as_percent_of_total_ag_land.csv
food_index_minion = DataParser('food_production_index.csv')
ag_machine_minion = DataParser('ag_machinery_per_km_arable_land.csv')
ag_land_minion = DataParser('agricultural_land_as_percent_total_land.csv')
arable_land_minion = DataParser('arable_land.csv')
fertilizer_minion = DataParser('fertilzer_consumption_per_hectare_arable_land.csv')
percent_emp_minion = DataParser('percent_employ_in_ag.csv')

##################################################################################################
####################### #  Graphing     ##########################################################
# minion.process_data()
# plt.figure(1)
# minion.graph_data(0)
# # plt.figure(2)
# minion.graph_data(1)
# # plt.figure(3)
# minion.graph_data(2)
# # plt.figure(4)
# minion.graph_data(3)
# minion.graph_data(4)
# minion.graph_data(5)

class CountryProfile:
    def __init__(self, country,food_index_minion,ag_machine_minion,ag_land_minion,arable_land_minion,fertilizer_minion,percent_emp_minion):
        self.country = country
        self.food_index_minion = food_index_minion
        self.ag_machine_minion = ag_machine_minion
        self.ag_land_minion = ag_land_minion
        self.arable_land_minion = arable_land_minion
        self.fertilizer_minion = fertilizer_minion
        self.percent_emp_minion = percent_emp_minion
    def display_country_details(self):
        print "COUNTRY DETAILS FOR: {}".format(self.country)
        self.food_data()
        self.ag_machine()
        self.ag_land()
        self.arable_land()
        self.fert()
        self.percent_emp()
    def food_data(self):
        print "     Food Index Data:"
        print "         average: {}".format(self.food_index_minion.processed_country_data[self.country]['average'])
        print "         maximum: {}".format(self.food_index_minion.processed_country_data[self.country]['maximum'])
        print "         minimum: {}".format(self.food_index_minion.processed_country_data[self.country]['minimum'])
    def ag_machine(self):
        print "     Agricultural Machinery Data:"
        print "         average: {}".format(self.ag_machine_minion.processed_country_data[self.country]['average'])
        print "         maximum: {}".format(self.ag_machine_minion.processed_country_data[self.country]['maximum'])
        print "         minimum: {}".format(self.ag_machine_minion.processed_country_data[self.country]['minimum'])
        
    def ag_land(self):
        print "     Agricultural Machinery Data:"
        print "         average: {}".format(self.ag_land_minion.processed_country_data[self.country]['average'])
        print "         maximum: {}".format(self.ag_land_minion.processed_country_data[self.country]['maximum'])
        print "         minimum: {}".format(self.ag_land_minion.processed_country_data[self.country]['minimum'])

    def arable_land(self):
        print "     Agricultural Machinery Data:"
        print "         average: {}".format(self.arable_land_minion.processed_country_data[self.country]['average'])
        print "         maximum: {}".format(self.arable_land_minion.processed_country_data[self.country]['maximum'])
        print "         minimum: {}".format(self.arable_land_minion.processed_country_data[self.country]['minimum'])

    def fert(self):
        print "     Agricultural Machinery Data:"
        print "         average: {}".format(self.fertilizer_minion.processed_country_data[self.country]['average'])
        print "         maximum: {}".format(self.fertilizer_minion.processed_country_data[self.country]['maximum'])
        print "         minimum: {}".format(self.fertilizer_minion.processed_country_data[self.country]['minimum'])

    def percent_emp(self):
        print "     Agricultural Machinery Data:"
        print "         average: {}".format(self.percent_emp_minion.processed_country_data[self.country]['average'])
        print "         maximum: {}".format(self.percent_emp_minion.processed_country_data[self.country]['maximum'])
        print "         minimum: {}".format(self.percent_emp_minion.processed_country_data[self.country]['minimum'])





class DataAggregator:
    def __init__(self, food_index_minion,ag_machine_minion,ag_land_minion,arable_land_minion,fertilizer_minion,percent_emp_minion):
        self.food_index_minion = food_index_minion
        self.ag_machine_minion = ag_machine_minion
        self.ag_land_minion = ag_land_minion
        self.arable_land_minion = arable_land_minion
        self.fertilizer_minion = fertilizer_minion
        self.percent_emp_minion = percent_emp_minion

        self.food_index_minion.process_data()
        self.ag_machine_minion.process_data()
        self.ag_land_minion.process_data()
        self.arable_land_minion.process_data()
        self.fertilizer_minion.process_data()
        self.percent_emp_minion.process_data()

    def most_potential(self):
        #most potential will have lowest fertilizer, lowest tractor, highest land, highest ag land
        print self


aggregator = DataAggregator(food_index_minion,ag_machine_minion,ag_land_minion,arable_land_minion,fertilizer_minion,percent_emp_minion)
aggregator.most_potential()

detailer = CountryProfile("France",food_index_minion,ag_machine_minion,ag_land_minion,arable_land_minion,fertilizer_minion,percent_emp_minion)
detailer.display_country_details()
