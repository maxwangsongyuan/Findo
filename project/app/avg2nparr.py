import numpy as np
import pandas as pd

def main():
    year = np.array([2010,2011,2012,2013,2014,2015,2016])
    df = pd.DataFrame(pd.read_csv(
        'average open price.csv', header=0))
    subset = df[df['symbol'] == "AFL"]
    AFL_price = np.array(subset['open'])

    subset = df[df['symbol'] == "CPB"]
    CPB_price = np.array(subset['open'])

    subset = df[df['symbol'] == "CA"]
    ACA_price = np.array(subset['open'])

    subset = df[df['symbol'] == "DISCA"]
    DISCA_price = np.array(subset['open'])

    subset = df[df['symbol'] == "HRB"]
    HRB_price = np.array(subset['open'])

    subset = df[df['symbol'] == "COG"]
    COG_price = np.array(subset['open'])

    subset = df[df['symbol'] == "EXPD"]
    EXPD_price = np.array(subset['open'])

    subset = df[df['symbol'] == "FAST"]
    FAST_price = np.array(subset['open'])

    subset = df[df['symbol'] == "HSIC"]
    HSIC_price = np.array(subset['open'])

    subset = df[df['symbol'] == "MLM"]
    MLM_price = np.array(subset['open'])



if __name__ == "__main__":
    main()
    print('Successful!')

