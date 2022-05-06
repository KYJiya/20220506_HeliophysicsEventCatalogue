import requests
import re
from bs4 import BeautifulSoup


def save_file(data):
    folder = ""
    filename = "FlareList_YYYYMMDD_HHMMSS.txt"
    
    f = open(folder+filename, 'w', encoding="utf-8")
    f.write(data)
    f.close()


def get_data():
    url = "http://hec.helio-vo.eu/hec/hec_gui_fetch.php"

    params = {
        "y_from": "2022",
        "mo_from": "4",
        "d_from": "6",
        "y_to": "2022",
        "mo_to": "5",
        "d_to": "6",
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
    redata = ""
    match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}[.]\d{1}.+', data)
    while match!=None:
        redata = redata + data[match.regs[0][0]:match.regs[0][1]] + '\n'
        data = data[match.regs[0][1]:]
        match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}[.]\d{1}.+', data)

    return redata


if __name__=="__main__":

    data = get_data()
    data = retail_data(data)

    save_file(data)