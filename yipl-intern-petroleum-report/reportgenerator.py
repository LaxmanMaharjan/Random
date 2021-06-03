"""Module for the solution of given Task.

Authur: Laxman Maharjan
Contact: lxmnmrzn@gmail.com
"""
import requests
import pandas as pd
import numpy as np
import sqlite3
pd.options.display.float_format = "{:,.2f}".format


class ReportGenerator:
    """This class generates the Petroleum Report as required."""

    def __init__(self, url):
        """Do Initialize the ReportGenerator class with url and dataset.

        Args:
            url: It is the url from where we get the json response of which
            we generate the report.
        """
        self.url = url
        self.get_dataset()

    def get_dataset(self):
        """Load the data and return respose.

        Return:
            response: It is the json response if request is successful
            else it return None and if exception occurs it return
            'Bad Response'
        """
        try:
            response = requests.get(url=self.url, timeout=1)
            if response.ok:
                # Original data is json reponse in pandas DataFrame object
                self.OriginalData = pd.DataFrame(response.json())
                return response
            else:
                return None
        except requests.exceptions.Timeout:
            return 'Bad Response'

    def database_actions(self):
        """Do all the database related task."""
        # creating database called report whose connection reference is
        # assigned to self.db
        try:
            self.db = sqlite3.connect("report.db")
        except Exception:
            print("Database connection Error")
        # creating sql Table to store the json response
        self.OriginalData.to_sql("Petroleum_Report", self.db,
                                 if_exists='replace',
                                 index=False)

        # Normalizing the dataset but i don't if it is exact normalization
        norm = self.OriginalData.pivot_table(index=['country', 'year'],
                                             columns=['petroleum_product'])
        names = self.convert_index(norm)

        norm.columns = names

        # storing Normalized form in db Table
        norm.to_sql("Normalized_form", self.db, if_exists='replace')

        # Retrieving dataset from database
        self.dataset = pd.read_sql_query("select * from petroleum_report",
                                         self.db)

    def convert_index(self, dataframe):
        """Do converts the multi-level index to single-level index.

        This function converts the mutli-level indes to single-level
        of the dataframe object passed as an argument.

        Args:
            dataframe: It is the dataframe object whose multi-level index needs
            to be converted into single-level index.
        Return:
            names: It is list of the single_level index.
        """
        # l0 contains value of level 0 index of dataframe
        # l1 contains value of level 1 index of dataframe
        l0 = dataframe.columns.get_level_values(0)
        l1 = dataframe.columns.get_level_values(1)
        names = [x[1] if x[1] else x[0] for x in zip(l0, l1)]
        return names

    def solution1(self):
        """Return overall sale of each petroleam product by country.

        This function finds overall sale of each petroleam product by country.

        Return:
            answer1: It is the DataFrame object which is list overall sale of
                     each petroleam product by country.
        """
        # converting country column to index and each petroleum product to
        # seperate columns
        answer1 = self.dataset.pivot_table(index=['country'],
                                           columns=['petroleum_product'],
                                           values=['sale'], aggfunc='sum')
        answer1.columns = self.convert_index(answer1)
        return answer1

    def solution2(self):
        """Return average sale of each petroleum product for 2 years of interval.

        Return:
            required: It is the DataFrame object which is List average sale of
            each petroleum product for 2 years of interval.
        """
        interval_avg = []
        interval = []
        # dataset1 is dataset where zero is replaced in np.nan(not a number)
        dataset1 = self.dataset.replace(0, np.nan)
        # so that we can drop nan which built-in function since zero is not
        # allowed to count while calculating average
        dataset1 = dataset1.dropna()

        # converting year column to index and each petroleum product to
        # seperate columns with sum of sales of each product as values in it.
        new = dataset1.pivot_table(index=['year'],
                                   columns=['petroleum_product'],
                                   values=['sale'], aggfunc='sum')
        new = new.replace(np.nan, 0)
        summation = new.to_numpy()
        # count is the DataFrame object with count of each petroleum product.
        count = dataset1.pivot_table(index=['year'],
                                     columns=['petroleum_product'],
                                     values=['sale'], aggfunc='count')
        non_empty = self.dataset.replace(0, np.nan).dropna()

        count = non_empty.pivot_table(index=['year'],
                                      columns=['petroleum_product'],
                                      values=['sale'], aggfunc='count')
        # nan can be replaced by any non zero number but it can't be
        # replaced by zero, esle dividion by zero error occurs
        count = count.replace(np.nan, 1)
        names = self.convert_index(count)

        count.columns = names

        total_count = count.to_numpy()
        avg = summation/total_count

        average = pd.DataFrame(avg, index=count.index,
                               columns=names).to_numpy()
        for i in range(0, 8, 2):
            interval_avg.append(average[i]+average[i+1])

        year_index = self.dataset['year'].unique()

        # formatting to represent in required format
        for i in range(0, 8, 2):
            interval.append(tuple(year_index[i:i+2]))
        ans = pd.DataFrame(interval_avg, index=interval, columns=names)
        ans = ans.reset_index()
        required = ans.melt(id_vars=['index'], value_vars=names,
                            var_name='Product', value_name='Average')
        required.rename(columns={'index': 'Year'}, inplace=True)
        required = required[['Product', 'Year', 'Average']]
        required = required.reset_index(drop=True)
        return required

    def solution3(self):
        """Return least sale each petroleum product and also its corresponding year.

        Return:
            It returns the DataFrame object which has required information.
        """
        # dict variable is to keep each petroleum product as key and it's
        # respective minimum values and year as values
        dict = {}

        wide_df = self.dataset.pivot_table(index=['petroleum_product'],
                                           columns=['year'], values=['sale'],
                                           aggfunc='sum')
        wide_df = wide_df.replace(0, np.nan)
        wide_df.columns = self.convert_index(wide_df)

        for index in wide_df.index:
            for i in wide_df.columns:
                if wide_df[i].loc[index] == wide_df.loc[index].min():
                    dict[index] = [wide_df.loc[index].min(), i]

        return pd.DataFrame(dict,
                            index=['Minimum Values', 'Corresponding Year'])


def main():
    """Do the solution of Task."""
    url = "https://raw.githubusercontent.com/younginnovations/"\
          "internship-challenges/master/programming/petroleum-report/data.json"

    r = ReportGenerator(url)
    r.database_actions()

    print(r.solution1())
    print("\n\nList of overall sale of each petroleam product by country:")

    print("\n\nList of average sale of each petroleum product for 2 years of"
          "interval:")
    print(r.solution2())

    print("\n\nList of Minimum sales of each petroleum product and it's"
          " corresponding values:")
    print(r.solution3())


if __name__ == '__main__':
    main()
