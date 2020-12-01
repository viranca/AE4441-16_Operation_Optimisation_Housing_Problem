
################################################################################################################
"""

"""

# Built-in/Generic Imports
import random
from math import sqrt

# Libs
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.stats import norm

# Own modules

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '01/12/2020'

################################################################################################################


class Dataset_abc:
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

    def plot_property_histogram(self, property, sub_property=None, bin_count=10):
        """
        Used to generate histogram of a specific property, using a provided number of bins

        :param property: Property of data to plot
        :param sub_property: Sub property if property has multiple sub-properties
        :param bin_count: Number of bins to use (set automatically for str properties)
        """

        # --> Create histogram plot
        property_lst = self.list_property(property, sub_property)

        if type(property_lst[0]) is str:
            num_bins = len(set(property_lst))

        else:
            num_bins = bin_count

        n, bins, patches = plt.hist(property_lst, num_bins,
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
