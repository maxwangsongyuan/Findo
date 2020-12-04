import pandas as pd
from sklearn import linear_model
import numpy as np
import numpy.linalg as la
import seaborn as sns

from .models import Test, StockInfo, FinancialProduct, StructuredFinancialInvestment
from .models import Users, UserClicks, UserSaves
from django.db import connection
from django.shortcuts import redirect

"""
Global
"""
c0 = 0
c1 = 0


def reg(price_arr, year_arr, seach_year):
    # df = pd.DataFrame(Stock_Market, columns=['Year', 'Month', 'Day', 'Price'])

    # X = df[['Year', 'Month', 'Day']]
    # Y = df['Price']

    # with sklearn
    regr = linear_model.LinearRegression()
    year_arr = year_arr.reshape(-1, 1)
    regr.fit(year_arr, price_arr)

    # print('Intercept: \n', regr.intercept_)
    # print('Coefficients: \n', regr.coef_)

    # x = New_Year
    # y = New_Month
    # z = New_Day
    # print('Predicted Stock Index Price: \n', regr.predict([[x, y, z]]))
    p = float(regr.intercept_) + float(seach_year) * float(regr.coef_)
    if regr.coef_ > 0:
        return ("The second model predicts the stock price to be" + str(p) + ". The stock is potentially good, buy it")
    if regr.coef_ <= 0:
        return ("The second model predicts the stock price to be" + str(p) + ". The stock is potentially bad, don't buy it")



def PCA_evaluation(Stock_Market):
    df = pd.DataFrame(Stock_Market, columns=['Year', 'Month', 'Open_Price', 'Close_Price'])

    A = df[['Open_Price', 'Close_Price']]

    new = A - np.mean(A, axis=0)

    U, S, Vt = np.linalg.svd(new, full_matrices=False)
    # Vstar = Vt[:,:].T             #using the first 2 principal components
    # Xstar=(new@Vstar)                 #change of basis     projection

    Xstar = (A @ Vt.T).values

    df['pc1'] = Xstar[:, 0]
    df['pc2'] = Xstar[:, 1]

    g1 = sns.lmplot('pc1', 'pc2', df, fit_reg=False, height=8, scatter_kws={"s": 180})
    ax = g1.axes[0, 0]
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')


def price_prediction_model_via_linear_least_square(price_arr, year_arr, seach_year):
    global c0, c1
    # print('-----------------------------------------------------------')
    # year = np.array([2010, 2011, 2012, 2013,2014,2015,2016])
    # df = pd.DataFrame(pd.read_csv('average open price.csv', header=0))
    # subset = df[df['symbol'] == "AFL"]
    # AFL_price = np.array(subset['open'])

    # year1 = np.array([2005, 2006, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015])
    # price1 = np.array([12, 41, 63, 72, 78, 80, 83, 88, 84, 90])

    # c1, c0 = la.lstsq(np.vstack([year1, np.ones(len(year1))]).T, price1)[0]

    c1, c0 = la.lstsq(np.vstack([year_arr, np.ones(len(year_arr))]).T, price_arr)[0]
    #
    # plt.scatter(year, price)
    # plt.plot(year, c1 * year + c0)
    #
    return c1 * int(seach_year) + c0


def searchFP(request):
    searchfp = request.POST.get('search_fp')

    for p in FinancialProduct.objects.raw('SELECT * FROM app_financialproduct where product_name = %s', [searchfp]):
        tmp = p


def main():
    Stock_Market = {
        'Year': [2017, 2017, 2017, 2017, 2017, 2017, 2017, 2017, 2017, 2017, 2017, 2017, 2016, 2016, 2016, 2016, 2016,
                 2016,
                 2016, 2016, 2016, 2016, 2016, 2016],
        'Month': [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        'Day': [12, 11, 10, 19, 28, 21, 21, 5, 24, 13, 22, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        'Price': [1464, 1394, 1357, 1293, 1256, 1254, 1234, 1195, 1159, 1167, 1130, 1075, 1047, 965, 943, 958,
                  971, 949, 884, 866, 876, 822, 704, 719]
    }
    New_Year = 2020
    New_Month = 12
    New_Day = 1
    reg(Stock_Market, New_Year, New_Month, New_Day)

    price_prediction_model_via_linear_least_square(2020)


if __name__ == '__main__':
    main()
