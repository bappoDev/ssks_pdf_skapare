from flask import Flask, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup

import requests
import json

app = Flask(__name__)
CORS(app)

gases = {
    "R12": 10900,
    "R1233zd": 4,
    "R1234yf": 4,
    "R1234ze": 7,
    "R125": 3500,
    "R1270": 2,
    "R134a": 1430,
    "R14": 7390,
    "R143a": 4470,
    "R152a": 124,
    "R161": 12,
    "R22": 1810,
    "R227ea": 3220,
    "R23": 14800,
    "R236fa": 9810,
    "R245fa": 1030,
    "R290": 1,
    "R32": 675,
    "R404A": 3922,
    "R407A": 2107,
    "R407B": 2804,
    "R407C": 1774,
    "R407D": 1627,
    "R407F": 1825,
    "R408A": 3152,
    "R410A": 2088,
    "R417A": 2346,
    "R417C": 1809,
    "R419A": 2967,
    "R422A": 3143,
    "R422D": 2729,
    "R423A": 2280,
    "R424A": 2440,
    "R426A": 1508,
    "R427A": 2138,
    "R428A": 3607,
    "R434A": 245,
    "R437A": 1805,
    "R438A": 2265,
    "R442A": 1888,
    "R448A": 1387,
    "R448C": 1250,
    "R449A": 1397,
    "R450A": 605,
    "R452A": 2140,
    "R452B": 692,
    "R453A": 1765,
    "R454B": 466,
    "R454C": 148,
    "R455A": 145,
    "R507A": 3985,
    "R508A": 13210,
    "R508B": 13400,
    "R513A": 631,
    "R515B": 293,
    "R600a": 3,
    "R717": 0,
    "R744": 1
}


def search(token, session_id, work_id):
    cookies = {
        'JSESSIONID': session_id,
        '.wgauth': token,
    }

    params = {
        'action': 'quickSearchPreventive',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'sv-SE,sv;q=0.9,en-SE;q=0.8,en-US;q=0.7,en;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'https://webgate.electroluxprofessional.com',
        'Referer': 'https://webgate.electroluxprofessional.com/serviceepr/3s/actHeaderList.do?action=navigateFilter&scrollTop=0',
        'Sec-Fetch-Dest': 'frame',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = [
        ('fieldsChanged', ''),
        ('filterField', 'x.NUMBER'),
        ('filterOperator', '='),
        ('filterValue', work_id),
        ('filterField1', ''),
        ('filterOperator1', '='),
        ('filterValue1', ''),
        ('searchDone', 'true'),
        ('dateType', 'APPROVAL'),
        ('dateFrom', ''),
        ('dateTo', ''),
        ('view0', 'on'),
        ('view1', 'on'),
        ('view2', 'on'),
        ('view10', 'on'),
        ('view3', 'on'),
        ('view4', 'on'),
        ('view9', 'on'),
        ('recordsPerPage', '50'),
        ('totalPages', '1'),
        ('currentPage', '1'),
        ('totalPages', '1'),
        ('totalRecords', '1'),
        ('editingNewRow', '0'),
        ('rowFieldsChanged', ''),
        ('enabledEdit', 'false'),
        ('scrollTop', '0'),
        ('showTab', ''),
        ('orderColumn', ''),
        ('orderType', ''),
        ('actType', '6'),
        ('additionalFilter', ''),
    ]

    response = requests.post(
        'https://webgate.electroluxprofessional.com/serviceepr/3s/actHeaderList.do',
        params=params,
        cookies=cookies,
        data=data,
        headers=headers
    )

    soup = BeautifulSoup(response.content, 'html.parser')
    data = []

    try:
        rows = soup.find_all('tr', {'class': 'rowWhite'})

        for row in rows:
            tds = row.find_all('td')
            name = tds[6].text
            actID = tds[6].get('onclick').split("'")[1].split("idAct=")[1]

            data.append({'name': name, 'actID': actID})

        return data
    except:
        return "Error: couldn't find acts linked to work id"


def row_info(token, session_id, act_id):
    cookies = {
        '.wgauth': token,
        'JSESSIONID': session_id
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'sv-SE,sv;q=0.9,en-SE;q=0.8,en-US;q=0.7,en;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'https://webgate.electroluxprofessional.com',
        'Referer': 'https://webgate.electroluxprofessional.com/serviceepr/3s/actRowsDetail.do?action=navigateFilter&scrollTop=1',
        'Sec-Fetch-Dest': 'frame',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'action': 'navigateFilter',
        'scrollTop': '0',
    }

    data = [
        ('fieldsChanged', ''),
        ('filterField', ''),
        ('filterOperator', 'contains'),
        ('filterValue', ''),
        ('view0', 'on'),
        ('view1', 'on'),
        ('recordsPerPage', '50'),
        ('totalPages', '1'),
        ('currentPage', '1'),
        ('totalPages', '1'),
        ('totalRecords', '3'),
        ('editingNewRow', '0'),
        ('rowFieldsChanged', ''),
        ('enabledEdit', 'false'),
        ('scrollTop', '0'),
        ('showTab', ''),
        ('orderColumn', ''),
        ('orderType', ''),
        ('idAct', act_id),
        ('idPnc', '0'),
        ('rowAction', ''),
        ('rowIdList', ''),
        ('idCustomerNew', '0'),
        ('rowNumNew', '0'),
        ('idPncFromList', '0'),
        ('multiselection', ''),
    ]

    response = requests.post(
        'https://webgate.electroluxprofessional.com/serviceepr/3s/actRowsDetail.do',
        params=params,
        cookies=cookies,
        headers=headers,
        data=data,
    )

    return response.content


def act_info(token, session_id, act_id):
    cookies = {
        'JSESSIONID': session_id,
        '.wgauth': token,
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'sv-SE,sv;q=0.9,en-SE;q=0.8,en-US;q=0.7,en;q=0.6',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Referer': 'https://webgate.electroluxprofessional.com/serviceepr/3s/actHeaderList.do?action=navigateFilter&scrollTop=0',
        'Sec-Fetch-Dest': 'frame',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'action': 'loadExisting',
        'idAct': act_id,
    }

    response = requests.get(
        'https://webgate.electroluxprofessional.com/serviceepr/3s/actHeaderDetail.do',
        params=params,
        cookies=cookies,
        headers=headers,
    )

    print(response.content)

    try:
        soup = BeautifulSoup(response.content, 'html.parser')

        fieldsets = soup.find_all("fieldset")

        customer_fieldsets = fieldsets[1].find_all("fieldset")
        customer_info_rows = customer_fieldsets[0].find_all('tr')

        first_row = customer_info_rows[0].find_all('td')
        fourth_row = customer_info_rows[3].find_all('td')

        customer_name = first_row[2].text.strip()
        customer_phone = first_row[4].text.strip()
        customer_email = fourth_row[4].text.strip()

        address_info_rows = customer_fieldsets[2].find_all('tr')

        first_row = address_info_rows[0].find_all('td')
        second_row = address_info_rows[1].find_all('td')

        address = second_row[1].text.strip()
        address_name = first_row[2].text.strip()

        work_fieldset = fieldsets[5]
        work_fieldset_rows = work_fieldset.find_all('tr')

        fifth_row = work_fieldset_rows[4].find_all('td')
        technician_name = fifth_row[4].text.strip().split(" ")[-1]

        new_html = row_info(token, session_id, act_id)
        soup = BeautifulSoup(new_html, 'html.parser')

        rows = soup.find_all('tbody', class_="rowWhite")

        gas_rows = []
        gas_sum = 0
        kg_sum = 0

        for row in rows:
            tr = row.find_all('tr')[0]
            td = tr.find_all('td')[3].text.split(' ')

            number = td[0]
            code = td[1]
            medium = td[2].upper()
            kg = td[3]

            gas_value = gases[medium]
            co2 = round((gas_value * int(kg)) / 1000, 2)

            gas_sum += co2
            kg_sum += int(kg)

            gas_rows.append({
                'number': number,
                'code': code,
                'medium': medium,
                'kg': kg,
                'co2': co2
            })

        data = {
            'customerName': customer_name,
            'customerEmail': customer_email,
            'address': address,
            'addressName': address_name,
            'technicianName': technician_name,
            'gasInfo': gas_rows,
            'gasSum': gas_sum,
            'kgSum': kg_sum
        }

        return data
    except:
        return "Error couldn't find act data"


@app.route('/search/<token>/<session_id>/<work_id>')
def get_search(token, session_id, work_id):
    data = search(token, session_id, work_id)
    return jsonify(data)


@app.route('/actinfo/<token>/<session_id>/<act_id>')
def get_act_info(token, session_id, act_id):
    data = act_info(token, session_id, act_id)
    return jsonify(data)


if __name__ == '__main__':
    app.run()
