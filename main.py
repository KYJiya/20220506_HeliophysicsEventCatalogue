import requests
import re
import os
from datetime import datetime as dt
from datetime import timezone as tz
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
import pandas as pd
from tqdm import tqdm


utc_now = dt.now(tz.utc)
before_one_month = utc_now - relativedelta(months=1)


def make_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def get_event_list_latest():
    url = "https://www.lmsal.com/solarsoft/latest_events/"
    
    data = pd.read_html(
        url,
        header=0,
    )

    return data


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
    filename = f"FlareList_{utc_now.astimezone().strftime('%Y%m%d_%H%M%S')}.txt"

    make_folder(folder)

    data_all = get_event_list_all()
    time_data = pd.to_datetime(data_all[0]["Snapshot Time"], utc=True)

    event_list = pd.DataFrame()
    data = get_event_list_latest()
    event_list = merge_event_list(event_list, data[0])
    for v in tqdm(time_data):
        if v >= before_one_month:
            data = get_event_list(v)
            event_list = merge_event_list(event_list, data[0])
        else:
            break

    event_list = event_list.iloc[::-1].reset_index(drop=True)
    event_list.to_csv(folder+filename, index=False)
    print(event_list)