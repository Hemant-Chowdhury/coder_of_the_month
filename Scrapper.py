from bs4 import BeautifulSoup
import requests
import json
import datetime
from urllib.request import urlopen
from dateutil.parser import parse
from User import User


class CF_Scrapper:

    def __init__(self):
        self.cf_contest = {}

    def scrape_contests(self, start_date, end_date):
        with urlopen("http://codeforces.com/api/contest.list?gym=false&format=json") as response:
            source = response.read()
            source = source.decode('utf-8').encode('cp850', 'replace').decode('cp850')
            data = json.loads(source)  # json.loads() creates dictionary from json data
            # js = json.dumps(data, indent=2) #json.dumps() creates a string from dict i.e dict to json converdion in python
            for contest in data['result']:
                if(contest['phase'] == 'FINISHED'):
                    # print(contest)
                    date = datetime.datetime.fromtimestamp(contest['startTimeSeconds'])
                    if start_date <= date <= end_date:
                        self.cf_contest[contest['id']] = date
            print(self.cf_contest)

    def scrape_user_submissions(self, user):
        cfLink = user.cf_url
        cfid = cfLink.split('/')[-1]
        # print(cfLink, cfid)
        try:
            source = requests.get(f'https://codeforces.com/contests/with/{cfid}').text
            soup = BeautifulSoup(source, 'lxml')
            soup = soup.decode('utf-8').encode('cp850', 'replace').decode('cp850')
            soup = BeautifulSoup(soup, 'lxml')
            # Looping over all contests participated by user in cf
            for tr in soup.find('div', class_='datatable').tbody.find_all('tr'):
                # cflist contain details related to user-contest in cf
                cflist = []
                # Extracting codeforces contestid
                str = tr.a.attrs['href'].split('/')
                cflist.insert(len(cflist), str[2])
                for td in tr.find_all('td'):
                    cflist.insert(len(cflist), td.text.strip())
                if int(cflist[0]) in self.cf_contest:
                    user.cf_sol += int(cflist[4])
        except Exception as e:
            print(e)


class CC_Scrapper:

    def __init__(self):
        self.cc_contest = {}

    def scrape_contests(self, start_date, end_date):
        source = requests.get('https://www.codechef.com/contests').text
        soup = BeautifulSoup(source, 'lxml')
        soup = soup.find('div', class_='content-wrapper')
        soup = soup.find_all('div')[4]
        for i in soup.tbody.find_all('tr'):
            clist = []
            for j in i.find_all('td'):
                clist.insert(len(clist), j.text)
            try:
                contest_type = clist[1].split(' ')[1]
                contest_end_time = parse(clist[2])
                if((start_date <= contest_end_time <= end_date) and (contest_type == "Challenge" or contest_type == "Cook-Off" or contest_type == "Lunchtime")):  # considering the required contests to be of the format <month name> <contest type> <year>
                    print(clist)
                    self.cc_contest[clist[0]] = clist[1]
            except Exception:
                pass

    def scrape_user_submissions(self, user):
        ccLink = user.cc_url
        ccid = ccLink.split('/')[-1]
        # print(ccLink, ccid)
        try:
            source = requests.get(f'https://www.codechef.com/users/{ccid}').text
            soup = BeautifulSoup(source, 'lxml')
            soup = soup.decode('utf-8').encode('cp850', 'replace').decode('cp850')
            soup = BeautifulSoup(soup, 'lxml')
            soup = soup.find('section', class_='rating-data-section problems-solved').article
            for p in soup.find_all('p'):
                cclist = [p.text.strip().split(":")]
                for c in cclist:
                    if self.cc_contest.get(c[0]) != None or self.cc_contest.get(c[0][:-1]) != None:
                        # print(c[0] + " = ", end='')
                        # print(len(c[1].split(',')))
                        user.cc_sol += len(c[1].split(','))
        except Exception as e:
            print(e)
