
################################################################################################################
"""

"""

# Built-in/Generic Imports
import random
from math import sqrt, ceil
from itertools import groupby
from copy import deepcopy

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
        #np.random.seed(2)
        #random.seed(345)
        return

    def list_property(self, property):
        property_lst = []

        for i in range(len(self.data)):
            property_lst.append(self.data[i][property])

        return property_lst

    def sort_by_property(self, property):
        """
        Use to sort data by property

        :param property:
        :return:
        """
        # --> Sorting using insertion sort (smallest to largest)
        for j in range(1, len(self.data)):
            for i in range(j, 0, -1):
                if self.data[i][property] < self.data[i - 1][property]:
                    self.data[i][property], self.data[i - 1][property] = \
                        self.data[i - 1][property], self.data[i][property]

        return

    def print_property_stats(self, property, bin_count=10):
        """
        Used to print statistical properties of a given property

        :param property: Property of data to plot
        :param bin_count: Number of bins to use (set automatically for str properties)
        """

        # --> Gather requested property
        property_lst, bin_count, bin_labels, binned_item_frequency = self.__get_property_stats(property,
                                                                                               bin_count=bin_count)

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

    def plot_property_histogram(self, property, bin_count=10):
        """
        Used to generate histogram of a specific property, using a provided number of bins

        :param property: Property of data to plot
        :param bin_count: Number of bins to use (set automatically for str properties)
        """

        # --> Gather requested property
        property_lst = self.list_property(property)

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
            plt.title(r"Histogram of " + property
                      + ": $\mu=$" + str(self.statistical_properties[property]["mu"])
                      + ", $\sigma=$" + str(self.statistical_properties[property]["sigma"]))

        else:
            plt.title(r"Histogram of " + property)

        plt.show()

    def __get_property_stats(self, property, bin_count=10):
        """
        Used to print statistical properties of a requested property, using a provided number of bins

        :param property: Property of data to plot
        :param bin_count: Number of bins to use (set automatically for str properties)
        """

        # --> Gather requested property
        property_lst = self.list_property(property)

        if type(property_lst[0]) is str:
            bin_count = len(set(property_lst))

        else:
            bin_count = bin_count

        # --> Get binned statistical properties
        if type(property_lst[0]) is str:
            property_lst.sort()

            binned_item_frequency = [len(list(group)) / len(property_lst) for key, group in groupby(property_lst)]

            bin_labels = list(set(property_lst))
            bin_labels.sort()

        else:
            binned_item_frequency = relfreq(property_lst, numbins=bin_count).frequency
            bin_size = (max(property_lst) - min(property_lst)) / bin_count
            bin_labels = []

            tracker = min(property_lst)

            for _ in range(bin_count):
                bin_labels.append(str(int(tracker)) + " <-> " + str(int(tracker + bin_size)))
                tracker += bin_size

        return property_lst, bin_count, bin_labels, binned_item_frequency

    def adjust_property_bin_by_percentage(self, property, bin_ref, percentage_change, bin_count=10):
        """
        Used to adjust a bin by a given percentage

        :param property: Property of data to plot
        :param bin_ref: The reference of the bin to change
        :param percentage_change: Percentage by which to change given bin (in %)
        :param bin_count: Number of bins to use (set automatically for str properties)
        """

        if percentage_change < -100:
            print("!!!!!!!!! Percentage change cannot be less than -100% !!!!!!!!!")
            return

        bin_ref -= 1

        # --> Define adjustment mode
        if percentage_change > 0:
            adjustment_mode = "Increase"

        else:
            adjustment_mode = "Decrease"

        # --> Gather requested property
        property_lst, bin_count, bin_labels, binned_item_frequency = self.__get_property_stats(property,
                                                                                               bin_count=bin_count)

        if percentage_change/100 * binned_item_frequency[bin_ref] + binned_item_frequency[bin_ref] > 1:
            print("!!!!!!!!! Percentage change makes bin frequency > 100% !!!!!!!!!")
            return

        binned_item_count = len(property_lst) * binned_item_frequency[bin_ref]
        nb_items_to_change = ceil(binned_item_count * abs(percentage_change) / 100)

        # --> Adjust dataset
        counter = 0
        while counter != nb_items_to_change:
            # --> Choose a random datapoint
            random_datapoint_ref = random.randint(0, len(self.data)-1)

            # --> For string properties
            if type(property_lst[0]) is str:

                # --> Change datapoint if datapoint matches bin to change/change mode
                if adjustment_mode == "Increase":
                    # --> If data point not in bin_ref to be adjusted
                    if self.data[random_datapoint_ref][property] != bin_labels[bin_ref]:
                        # --> Set to ref_bin
                        self.data[random_datapoint_ref][property] = bin_labels[bin_ref]

                        # --> Increase counter
                        counter += 1

                    else:
                        pass

                elif adjustment_mode == "Decrease":
                    # --> If self.data point in bin_ref to be adjusted
                    if self.data[random_datapoint_ref][property] == bin_labels[bin_ref]:
                        # --> Select a new bin that is not the ref_bin
                        available_bins = deepcopy(bin_labels)
                        available_bins.remove(bin_labels[bin_ref])

                        self.data[random_datapoint_ref][property] = \
                            random.choice(available_bins)

                        # --> Increase counter
                        counter += 1

                    else:
                        pass

            # --> For int properties
            else:
                bin_ref_label_formatted = self.__format_bin_label(bin_labels[bin_ref])

                # --> Change datapoint if datapoint matches bin to change/change mode
                if adjustment_mode == "Increase":
                    print(bin_ref_label_formatted)
                    if self.data[random_datapoint_ref][property] < bin_ref_label_formatted[0] \
                            or self.data[random_datapoint_ref][property] > bin_ref_label_formatted[1]:
                        self.data[random_datapoint_ref][property] = random.randint(bin_ref_label_formatted[0],
                                                                                   bin_ref_label_formatted[1])

                        # --> Increase counter
                        counter += 1

                    else:
                        pass

                elif adjustment_mode == "Decrease":
                    # --> If self.data point in bin_ref to be adjusted
                    if bin_ref_label_formatted[0] <= self.data[random_datapoint_ref][property] <= bin_ref_label_formatted[1]:
                        # --> Select a new bin that is not the ref_bin
                        available_bins = deepcopy(bin_labels)
                        available_bins.remove(bin_labels[bin_ref])

                        new_bin_range = self.__format_bin_label(random.choice(available_bins))
                        self.data[random_datapoint_ref][property] = random.randint(new_bin_range[0], new_bin_range[1])

                        # --> Increase counter
                        counter += 1

                    else:
                        pass

        print("=========================================================== Dataset adjustment successful")
        print("Dataset new statistical properties:")
        self.print_property_stats(property, bin_count)

        return

    @staticmethod
    def __format_bin_label(label):
        label_formatted = label.split(" <-> ")
        label_formatted = [int(i) for i in label_formatted]
        return label_formatted

