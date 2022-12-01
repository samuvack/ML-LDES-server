from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas.io.sql as sqlio
from sklearn.metrics import r2_score

# Python
def stan_init(m):
    """Retrieve parameters from a trained model.

    Retrieve parameters from a trained model in the format
    used to initialize a new Stan model.

    Parameters
    ----------
    m: A trained model of the Prophet class.

    Returns
    -------
    A Dictionary containing retrieved parameters of m.

    """
    res = {}
    for pname in ['k', 'm', 'sigma_obs']:
        res[pname] = m.params[pname][0][0]
    for pname in ['delta', 'beta']:
        res[pname] = m.params[pname][0]
    return res


df = pd.read_csv(
    'https://raw.githubusercontent.com/facebook/prophet/main/examples/example_wp_log_peyton_manning.csv')
df1 = df.loc[df['ds'] < '2016-01-19', :]  # All data except the last day
m1 = Prophet().fit(df1)  # A model fit to all data except the last day


m2 = Prophet().fit(df)  # Adding the last day, fitting from scratch
# Adding the last day, warm-starting from m1
m2 = Prophet().fit(df, init=stan_init(m1))
