import requests
import re
import os
from datetime import datetime
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta


now = datetime.now()
before_one_month = now - relativedelta(months=1)


def save_file(data):
    folder = "data/"
    filename = f"FlareList_{now.strftime('%Y%m%d_%H%M%S')}.txt"
    
    if not os.path.exists(folder): os.makedirs(folder)

    f = open(folder+filename, 'w', encoding="utf-8")
    f.write(data)
    f.close()


def get_data():
    url = "http://hec.helio-vo.eu/hec/hec_gui_fetch.php"

    params = {
        "y_from": before_one_month.year,
        "mo_from": before_one_month.month,
        "d_from": before_one_month.day,
        "y_to": now.year,
        "mo_to": now.month,
        "d_to": now.day,
        "radioremote": "on",
        "titlesearch2": "",
        "gevloc_sxr_flare": "istable",
    }

    response = requests.get(
        url,
        params = params,
    )

    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    data = soup.body.get_text().strip()

    return data


def retail_data(data):
    retailed_data = ""
    match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}[.]\d{1}.+', data)
    while match!=None:
        match_data = data[match.regs[0][0]:match.regs[0][1]]
        match_start = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', match_data)
        match_start_datetime = datetime.strptime(match_data[match_start.regs[0][0]:match_start.regs[0][1]], "%Y-%m-%d %H:%M:%S")
        match_end_data = match_data[match_start.regs[0][1]:]
        match_end = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', match_end_data)
        match_end_datetime = datetime.strptime(match_end_data[match_end.regs[0][0]:match_end.regs[0][1]], "%Y-%m-%d %H:%M:%S")

        # DELETE the row outside specific time
        if before_one_month < match_start_datetime and match_end_datetime < now:
            retailed_data = retailed_data + match_data + '\n'
            
        data = data[match.regs[0][1]:]
        match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}[.]\d{1}.+', data)

    return retailed_data


if __name__=="__main__":

    data = get_data()
    data = retail_data(data)

    save_file(data)