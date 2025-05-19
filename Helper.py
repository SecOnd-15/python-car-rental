from Dashboard.DashboardMainApp import Dashboard
import matplotlib.pyplot as plt


# Diri i butang ang mga helper methods
class Helper():

    # DEPRECATED (OLD FUNCTION WA NAY PULOS)
    @staticmethod
    def is_empty_or_whitespace(input_string):
        return input_string.strip() == ""
    

    @staticmethod
    def after_login():
        Dashboard()
      

  