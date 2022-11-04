from river import datasets
from river import metrics
from river import time_series
import datetime as dt
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Process, Queue


from multiprocessing import Process, Queue
from stage2 import Stage2
import time
import random

class Stage1:

    def stage1(self, queueS1):
        print("stage1")
        file_names = []

        for j in range(143):
            dataset = datasets.AirlinePassengers()

            model = time_series.HoltWinters(
            alpha=0.3,
            beta=0.1,
            gamma=0.6,
            seasonality=12,
            multiplicative=True
            )

            """
            alpha: Smoothing parameter for the level.
            beta  (defaults to None): Smoothing parameter for the trend.
            gamma (defaults to None): Smoothing parameter for the seasonality.
            seasonality (defaults to 0): The number of periods in a season. For instance, this should be 4 for quarterly data, and 12 for yearly data.
            multiplicative (defaults to False): Whether or not to use a multiplicative formulation.
            """

            metric = metrics.MAE()

            time_series.evaluate(
            dataset,
            model,
            metric,
            horizon=12
            )

            horizon=12

            prediction = 0
            forecast = [1]
            
            q=0
            for t, (x, y) in enumerate(datasets.AirlinePassengers()):
                t_list2=[]
                #print('error:', (forecast[0] - prediction))
                model = model.learn_one(float(y))
                print(y)               
                forecast = model.forecast(horizon=horizon)

                visualise_data = forecast
                visualise_data.insert(0, y)
                queueS1.put(visualise_data) #Send it into queue



                #print(forecast)
                prediction = y
                for i in range(len(forecast)):
                    t_list2.append(t+i)

                if (q==j):
                    plt.figure()
                    sns.set()
                    x_list=[]
                    y_list=[]
                    t_list=[]
                    for t, (x, y) in enumerate(datasets.AirlinePassengers()):
                        x_list.append(x)
                        y_list.append(y)
                        t_list.append(t)
                    plt.scatter(t_list, y_list, c='r', alpha=0.6, s=4)
                    plt.plot(t_list, y_list, linewidth=0.3)
                    plt.plot(t_list2, forecast)
                    plt.suptitle("Online Machine Learning (forecasting)", fontsize=18)
                    plt.title("Iteration {y}".format(y=q), fontsize=10)
                    plt.xlabel('Time')
                    plt.ylabel('Value')
                    plt.savefig("../images/it_{y}.png".format(y=q))
                    print("../images/it_{y}.png".format(y=q))
                    file_names.append("../images/it_{y}.png".format(y=q))
                q = q+ 1
                time.sleep(3)
                    
        import imageio
        images = []
        for filename in file_names:
            images.append(imageio.imread(filename))
        imageio.mimsave('../images/movie.gif', images)
        

        """

            future = [{'month': dt.date(year=1961, month=m, day=1)}
            for m in range(1, horizon + 1)
            ]



            for x, y_pred in zip(future, forecast):
                print(x['month'], f'{y_pred:.3f}')
        """
        

if __name__ == '__main__':


   
    s1= Stage1()
    s2= Stage2()
    stage2.start_app()

    # S1 to S2 communication
    queueS1 = Queue()  # s1.stage1() writes to queueS1


    # start s2 as another process
    s2 = Process(target=s2.stage2, args=(queueS1,))
    s2.daemon = True
    s2.start()     # Launch the stage2 process

    s1.stage1(queueS1) # start sending stuff from s1 to s2 
    s2.join() # wait till s2 daemon finishes

