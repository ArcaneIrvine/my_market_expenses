import collections
import yaml
import os
import math
import numpy as np
import matplotlib.ticker
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
from collections import Counter

# every date in data
date = []
# every price of each day
price_daily = []

# every product in data
product = []
# every date in which each product was given
product_date = []
# each price of every product
price = []


# import market_data file
with open(os.path.dirname(os.path.abspath(__file__)) + "/data/market_data.yaml", "r") as file:
    data = yaml.safe_load(file)

# seperate the data into lists
for item1 in data['market']:
    for item2 in item1['products']:
        product.append(item2)
        product_date.append(item1['date'])
    for item3 in item1['price']:
        price.append(item3)
        if item1['date'] not in date:
            date.append(item1['date'])
            price_daily.append(round(math.fsum(item1['price']), 2))


# plot the data
def plot():
    fig, ax = plt.subplots()
    mean = np.mean(price_daily)

    ax.scatter(date, price_daily, color='black')
    ax.plot(date, price_daily, color='grey')
    ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(0.8))
    ax.axhline(y=np.nanmean(price_daily), color='red', linestyle='--', linewidth=2, label='avg')

    # show value of each point
    for index in range(len(date)):
        ax.text(date[index], price_daily[index], price_daily[index], size=10)

    # show avg line value
    trans = transforms.blended_transform_factory(
        ax.get_yticklabels()[0].get_transform(), ax.transData)
    ax.text(0, mean, "{:.0f}".format(mean), color="red", transform=trans, ha="right", va="center")

    # print the plot
    fig.autofmt_xdate()
    plt.legend(loc='best')
    plt.savefig('figures/fig.png', dpi=300)


# plot the bar
def bar():
    # counter for products, count how many times each product shows up
    count = dict(Counter(product))
    sorted_x = sorted(count.items(), key=lambda kv: kv[1], reverse=True)
    sorted_count = collections.OrderedDict(sorted_x)
    count_a = list(sorted_count.keys())
    count_b = list(sorted_count.values())
    # count_b.sort(reverse=True)

    fig, ax = plt.subplots()
    plt.bar(count_a, count_b, color='grey')
    ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(1))
    fig.autofmt_xdate(rotation=45)
    plt.savefig('figures/plot.png', dpi=300)


plot()
bar()
