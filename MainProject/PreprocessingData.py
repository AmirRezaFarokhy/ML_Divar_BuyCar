import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt


class Preprocess:

    def RemoveOutliers(self, main_df, col, threshold):
        sns.boxenplot(main_df[col])
        plt.title(f'Original Plot of {col}')
        plt.show()

        self.removed_outlier = main_df[main_df[col] >= threshold]

        sns.boxplot(self.removed_outlier[col])
        plt.title(f'Plot without Outliers of {col}')
        plt.show()

        return self.removed_outlier


