
################################################################################################################
"""

"""

# Built-in/Generic Imports
import random
from math import sqrt
from itertools import groupby

# Libs
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

from scipy.stats import norm, cumfreq, itemfreq, binned_statistic, relfreq

# Own modules

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '01/12/2020'

################################################################################################################


class Dataset:
    def __init__(self):
        # --> Seeding generators
        np.random.seed(2)
        random.seed(345)

    def list_property(self, property, sub_property=None):
        property_lst = []

        if sub_property is None:
            for i in range(len(self.data)):
                property_lst.append(self.data[i][property])

        else:
            for i in range(len(self.data)):
                property_lst.append(self.data[i][property][sub_property])

        return property_lst

    def sort_by_property(self, property):
        # --> Sorting using insertion sort (smallest to largest)
        for j in range(1, len(self.data)):
            for i in range(j, 0, -1):
                if self.data[i][property] < self.data[i - 1][property]:
                    self.data[i][property], self.data[i - 1][property] = \
                        self.data[i - 1][property], self.data[i][property]

    # def post_process(self, property, bin_ref, percent_change, bin_count=10, sub_property=None):

    def get_property_stats(self, property, bin_count=10, sub_property=None):
        """
        Used to print statistical properties of a requested property, using a provided number of bins

        :param property: Property of data to plot
        :param sub_property: Sub property if property has multiple sub-properties
        :param bin_count: Number of bins to use (set automatically for str properties)
        """

        # --> Gather requested property
        property_lst = self.list_property(property, sub_property)

        if type(property_lst[0]) is str:
            bin_count = len(set(property_lst))

        else:
            bin_count = bin_count

        # --> Get binned statistical properties
        if type(property_lst[0]) is str:
            property_lst.sort()

            binned_item_frequency = [len(list(group))/len(property_lst) for key, group in groupby(property_lst)]

            bin_labels = list(set(property_lst))
            bin_labels.sort()

        else:
            binned_item_frequency = relfreq(property_lst, numbins=bin_count).frequency
            bin_size = (max(property_lst) - min(property_lst))/bin_count
            bin_labels = []

            tracker = min(property_lst)

            for _ in range(bin_count):
                bin_labels.append(str(int(tracker)) + " <-> " + str(int(tracker + bin_size)))
                tracker += bin_size

        # --> Print statistical properties
        print("================ " + property)
        # print(property_lst)
        # print("\n")

        print("Bin count:", bin_count)
        for i in range(bin_count):
            print("Ref:", i+1, "->   Bin:", bin_labels[i], "    Freq:", binned_item_frequency[i])

        print("\n")

        if property in self.statistical_properties.keys():
            print("Distribution type: Normal")
            print("   - Mu:", str(self.statistical_properties[property]["mu"]))
            print("   - Sigma:", str(self.statistical_properties[property]["sigma"]))

        else:
            print("Distribution type: Random")

        print("\n")
        return

    def plot_property_histogram(self, property, bin_count=10, sub_property=None):
        """
        Used to generate histogram of a specific property, using a provided number of bins

        :param property: Property of data to plot
        :param sub_property: Sub property if property has multiple sub-properties
        :param bin_count: Number of bins to use (set automatically for str properties)
        """

        # --> Gather requested property
        property_lst = self.list_property(property, sub_property)

        if type(property_lst[0]) is str:
            bin_count = len(set(property_lst))
        else:
            bin_count = bin_count

        # --> Create histogram plot
        n, bins, patches = plt.hist(property_lst, bin_count,
                                    # density=1,
                                    facecolor='blue')

        # # --> Add a 'best fit' line
        # if property in self.statistical_properties.keys():
        #     y = norm.pdf(bins,
        #                  self.statistical_properties[property]["mu"],
        #                  self.statistical_properties[property]["sigma"])
        #     plt.plot(bins, y, 'r--')

        # --> Add plot info/LABELS
        plt.xlabel(property)
        plt.ylabel('Frequency')

        if property in self.statistical_properties.keys():
            if sub_property is None:
                plt.title(r"Histogram of " + property
                          + ": $\mu=$" + str(self.statistical_properties[property]["mu"])
                          + ", $\sigma=$" + str(self.statistical_properties[property]["sigma"]))

            else:
                plt.title(r"Histogram of " + property + " " + sub_property
                          + ": $\mu=$" + str(self.statistical_properties[property]["mu"])
                          + ", $\sigma=$" + str(self.statistical_properties[property]["sigma"]))

        else:
            if sub_property is None:
                plt.title(r"Histogram of " + property)

            else:
                plt.title(r"Histogram of " + property + " " + sub_property)

        plt.show()
