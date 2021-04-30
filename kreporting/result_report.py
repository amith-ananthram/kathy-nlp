import os
import pandas as pd


class ResultReport:
    def __init__(self, investigation):
        self.investigation = investigation
        self.filename = '%s-results.csv' % self.investigation

        if os.path.exists(self.filename):
            self.df = pd.read_csv(self.filename)
        else:
            self.df = pd.DataFrame()

    def add_results(self, results):
        self.df = self.df.append(results, ignore_index=True)
        self.df.to_csv(self.filename, index=False)
