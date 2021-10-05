import csv
import json
import os
import threading
import time
import traceback

# import requests
import cfscrape

url = 'https://www.myus.com/_/ShippingRate/CalculateShippingRate'
header = ["Code", "Country", "Weight", "Company", "Days", "Shipping", "Currency"]
threadcount = 1
semaphore = threading.Semaphore(threadcount)
write = threading.Lock()
out_file = 'out.csv'
error_file = "error.csv"
services = ["FedEx Economy", "DHL Express", "Budget Economy"]

rows = []


def get(params, country, wt, state=None):
    semaphore.acquire()
    try:
        params['countryCode'] = country
        params['weight'] = wt
        if state is not None:
            params['state'] = state
        text = cfscrape.CloudflareScraper().post(url, params=params).text
        if "Access Denied" in text:
            print('Access Denied', country, wt)
            semaphore.release()
            get(params, country, wt, state)
            return
        js = json.loads(text)
        for shipping in js['data']['shippingRates']:
            if shipping['service'] in services:
                data = {
                    "Code": country if country != "US" else f"{country}-{state}",
                    "Country": countries[country] if country != "US" else f"{countries[country]}-{states[state]}",
                    "Weight": wt,
                    "Company": shipping['service'],
                    "Days": shipping['serviceEstimatedDelivery'].replace('-', '_'),
                    "Shipping": "",
                    "Currency": "USD"
                }
                ship = shipping['standardRate']
                data['Company'] = f"{shipping['service']} Standard"
                data['Shipping'] = ship['amountUsd']
                print(json.dumps(data, indent=4))
                rows.append(data)
        with open('out.json', 'w') as out_file:
            json.dump(rows, out_file, indent=4)
            # append(data.copy())
    except:
        append_error([country, wt])
        print([country, wt])
        traceback.print_exc()
    semaphore.release()


def main():
    os.system('color 0a')
    logo()
    params = {
        "countryCode": "US",
        "weight": "1",
        "currencyCode": "USD",
        "lang": "en",
        "facilityid": "1",
        "length": "0",
        "width": "0",
        "height": "0"
    }
    if not os.path.isfile(out_file):
        with open(out_file, 'w', encoding='utf8', newline='') as ofile:
            csv.DictWriter(ofile, fieldnames=header).writeheader()
    threads = []
    for country in countries.keys():
        # for country in ['US']:
        for i in range(1, 200):
            if country == 'US':
                for state in states.keys():
                    # get(params.copy(), country, i, state)
                    t = threading.Thread(target=get, args=(params.copy(), country, i, state,))
                    t.start()
                    threads.append(t)
                    time.sleep(0.5)
            else:
                get(params.copy(), country, i)
                time.sleep(0.5)
                # t = threading.Thread(target=get, args=(params.copy(), country, i,))
                # t.start()
                # threads.append(t)
    for thread in threads:
        thread.join()


def append(row):
    with write:
        with open(out_file, 'a', encoding='utf8', newline='') as ofile:
            csv.DictWriter(ofile, fieldnames=header).writerow(row)


def append_error(row):
    with write:
        with open(error_file, 'a', encoding='utf8', newline='') as efile:
            csv.writer(efile).writerow(row)


def logo():
    print("""
        __  ___        __  __ _____                         
       /  |/  /__  __ / / / // ___/   _____ ____   ____ ___ 
      / /|_/ // / / // / / / \__ \   / ___// __ \ / __ `__ \\
     / /  / // /_/ // /_/ / ___/ /_ / /__ / /_/ // / / / / /
    /_/  /_/ \__, / \____/ /____/(_)\___/ \____//_/ /_/ /_/ 
            /____/                                          
===================================================================
      MyUS.com price scraper by: fiverr.com/muhammadhassan7
===================================================================
[+] Multithreaded
[+] CSV Output
[+] JSON output
___________________________________________________________________
""")


states = {
    "AA": "Armed Forces Americas",
    "AE": "Armed Forces Europe",
    "AK": "Alaska",
    "AL": "Alabama",
    "AP": "Armed Forces Pacific",
    "AR": "Arkansas",
    "AZ": "Arizona",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DC": "District of Columbia",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "IA": "Iowa",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "MA": "Massachusetts",
    "MD": "Maryland",
    "ME": "Maine",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MO": "Missouri",
    "MS": "Mississippi",
    "MT": "Montana",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "NE": "Nebraska",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NV": "Nevada",
    "NY": "New York",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VA": "Virginia",
    "VT": "Vermont",
    "WA": "Washington",
    "WI": "Wisconsin",
    "WV": "West Virginia",
    "WY": "Wyoming",
}

countries = {
    "AL": "Albania",
    "DZ": "Algeria",
    "AS": "American Samoa",
    "AD": "Andorra",
    "AO": "Angola",
    "AI": "Anguilla",
    "AG": "Antigua & Barbuda",
    "AR": "Argentina",
    "AM": "Armenia",
    "AW": "Aruba",
    "AU": "Australia",
    "AT": "Austria",
    "AZ": "Azerbaijan",
    "BS": "Bahamas",
    "BH": "Bahrain",
    "BD": "Bangladesh",
    "BB": "Barbados",
    "BY": "Belarus",
    "BE": "Belgium",
    "BZ": "Belize",
    "BJ": "Benin",
    "BM": "Bermuda",
    "BT": "Bhutan",
    "BO": "Bolivia",
    "XB": "Bonaire",
    "BA": "Bosnia & Herzegovina",
    "BW": "Botswana",
    "BR": "Brazil",
    "VG": "British Virgin Islands",
    "BN": "Brunei",
    "BG": "Bulgaria",
    "BF": "Burkina Faso",
    "BI": "Burundi",
    "KH": "Cambodia",
    "CM": "Cameroon",
    "CA": "Canada",
    "IC": "Canary Islands",
    "CV": "Cape Verde",
    "KY": "Cayman Islands",
    "CF": "Central African Republic",
    "TD": "Chad",
    "CL": "Chile",
    "CN": "China",
    "CO": "Colombia",
    "KM": "Comoros",
    "CG": "Congo",
    "CD": "Congo, DRC",
    "CK": "Cook Islands",
    "CR": "Costa Rica",
    "HR": "Croatia",
    "XC": "Curacao",
    "CY": "Cyprus",
    "CZ": "Czech Republic",
    "DK": "Denmark",
    "DJ": "Djibouti",
    "DM": "Dominica",
    "DO": "Dominican Republic",
    "TP": "East Timor",
    "EC": "Ecuador",
    "EG": "Egypt",
    "SV": "El Salvador",
    "GQ": "Equatorial Guinea",
    "ER": "Eritrea",
    "EE": "Estonia",
    "ET": "Ethiopia",
    "FK": "Falkland Islands",
    "FO": "Faroe Islands",
    "FJ": "Fiji",
    "FI": "Finland",
    "FR": "France",
    "GF": "French Guiana",
    "GA": "Gabon",
    "GM": "Gambia",
    "GE": "Georgia",
    "DE": "Germany",
    "GH": "Ghana",
    "GI": "Gibraltar",
    "GR": "Greece",
    "GL": "Greenland",
    "GD": "Grenada",
    "GP": "Guadeloupe",
    "GU": "Guam",
    "GT": "Guatemala",
    "GG": "Guernsey",
    "GW": "Guinea Bissau",
    "GN": "Guinea Republic",
    "GY": "Guyana",
    "HT": "Haiti",
    "HN": "Honduras",
    "HK": "Hong Kong",
    "HU": "Hungary",
    "IS": "Iceland",
    "IN": "India",
    "ID": "Indonesia",
    "IQ": "Iraq",
    "IE": "Ireland",
    "IL": "Israel",
    "IT": "Italy",
    "CI": "Ivory Coast",
    "JM": "Jamaica",
    "JP": "Japan",
    "JE": "Jersey",
    "JO": "Jordan",
    "KZ": "Kazakhstan",
    "KE": "Kenya",
    "KI": "Kiribati",
    "KV": "Kosovo",
    "KW": "Kuwait",
    "KG": "Kyrgyzstan",
    "LA": "Laos",
    "LV": "Latvia",
    "LB": "Lebanon",
    "LS": "Lesotho",
    "LR": "Liberia",
    "LI": "Liechtenstein",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "MO": "Macau",
    "MK": "Macedonia",
    "MG": "Madagascar",
    "MW": "Malawi",
    "MY": "Malaysia",
    "MV": "Maldives",
    "ML": "Mali",
    "MT": "Malta",
    "MH": "Marshall Islands",
    "MQ": "Martinique",
    "MR": "Mauritania",
    "MU": "Mauritius",
    "YT": "Mayotte",
    "MX": "Mexico",
    "FM": "Micronesia",
    "MD": "Moldova",
    "MC": "Monaco",
    "MN": "Mongolia",
    "ME": "Montenegro",
    "MS": "Montserrat",
    "MA": "Morocco",
    "MZ": "Mozambique",
    "NA": "Namibia",
    "NR": "Nauru",
    "NP": "Nepal",
    "NL": "Netherlands",
    "XN": "Nevis",
    "NC": "New Caledonia",
    "NZ": "New Zealand",
    "NI": "Nicaragua",
    "NE": "Niger",
    "NG": "Nigeria",
    "NU": "Niue",
    "MP": "Northern Mariana Islands",
    "NO": "Norway",
    "OM": "Oman",
    "PK": "Pakistan",
    "PW": "Palau",
    "PA": "Panama",
    "PG": "Papua New Guinea",
    "PY": "Paraguay",
    "PE": "Peru",
    "PH": "Philippines",
    "PL": "Poland",
    "PT": "Portugal",
    "PR": "Puerto Rico",
    "QA": "Qatar",
    "RE": "Reunion Island",
    "RO": "Romania",
    "RU": "Russia",
    "RW": "Rwanda",
    "AN": "Saba",
    "WS": "Samoa",
    "ST": "Sao Tome",
    "SA": "Saudi Arabia",
    "SN": "Senegal",
    "RS": "Serbia",
    "SC": "Seychelles",
    "SL": "Sierra Leone",
    "SG": "Singapore",
    "SK": "Slovakia",
    "SI": "Slovenia",
    "SB": "Solomon Islands",
    "SO": "Somalia",
    "XS": "Somaliland Rep",
    "ZA": "South Africa",
    "KR": "South Korea",
    "SS": "South Sudan",
    "ES": "Spain",
    "LK": "Sri Lanka",
    "VC": "St Vincent",
    "XY": "St. Barthelemy",
    "XE": "St. Eustatius",
    "KN": "St. Kitts",
    "LC": "St. Lucia",
    "XM": "St. Maarten",
    "SR": "Suriname",
    "SZ": "Swaziland",
    "SE": "Sweden",
    "CH": "Switzerland",
    "PF": "Tahiti & French Polynesia",
    "TW": "Taiwan",
    "TZ": "Tanzania",
    "TH": "Thailand",
    "TG": "Togo",
    "TO": "Tonga",
    "TT": "Trinidad & Tobago",
    "TN": "Tunisia",
    "TR": "Turkey",
    "TC": "Turks & Caicos",
    "TV": "Tuvalu",
    "UG": "Uganda",
    "UA": "Ukraine",
    "AE": "United Arab Emirates",
    "GB": "United Kingdom",
    "US": "United States",
    "UY": "Uruguay",
    "VI": "US Virgin Islands",
    "UZ": "Uzbekistan",
    "VU": "Vanuatu",
    "VE": "Venezuela",
    "VN": "Vietnam",
    "YE": "Yemen",
    "ZM": "Zambia",
    "ZW": "Zimbabwe"
}

if __name__ == '__main__':
    main()
