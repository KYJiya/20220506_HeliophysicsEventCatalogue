import requests
import re
import os
from datetime import datetime as dt
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
import pandas as pd
from tqdm import tqdm


now = dt.now()
before_one_month = now - relativedelta(months=1)


def save_file(folder, filename, data):
    if not os.path.exists(folder):
        os.makedirs(folder)

    f = open(folder + filename, "w", encoding="utf-8")
    f.write(data)
    f.close()


def get_event_list_all():
    url = "https://www.lmsal.com/solarsoft/latest_events_archive.html"
    
    data = pd.read_html(
        url,
        header=0,
    )

    return data


def get_event_list(time_data):
    url = "https://www.lmsal.com/solarsoft/ssw/last_events-" + \
            time_data.strftime("%Y") + \
            "/last_events_" + \
            time_data.strftime("%Y%m%d") + "_" + time_data.strftime("%H%M") + \
            "/index.html"

    data = pd.read_html(
        url,
        header=0,
    )

    return data


def merge_event_list(event_list, data):
    data = data.drop(["Event#","EName"], axis=1)
    data = data[data["Derived Position"].str.contains('\d{4}')]
    event_list = pd.concat([data, event_list])
    event_list = event_list.drop_duplicates(["Start","Stop","Peak","GOES Class","Derived Position"])
    event_list = event_list.reset_index(drop=True)

    return event_list
    

if __name__ == "__main__":
    folder = "data/"
    filename = f"FlareList_{now.strftime('%Y%m%d_%H%M%S')}.txt"

    data_all = get_event_list_all()
    time_data = pd.to_datetime(data_all[0]["Snapshot Time"])

    event_list = pd.DataFrame()
    for v in tqdm(time_data):
        if v >= before_one_month:
            data = get_event_list(v)
            event_list = merge_event_list(event_list, data[0])
        else:
            break

    event_list = event_list.iloc[::-1].reset_index(drop=True)

    print(event_list)