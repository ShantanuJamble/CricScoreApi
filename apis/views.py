import collections
import requests
from bs4 import BeautifulSoup


# Create your views here.


class WebScrapper(object):
    url = ''
    headers = {}

    def __init__(self):
        self.url = "http://www.espncricinfo.com/"
        self.headers = {"user-agent": "Mozilla/5.0",}

    def get_all_games(self):
        new_url = self.url + "ci/engine/match/index.html"
        resp = requests.get(new_url, headers=self.headers)
        # print resp.content
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            # fetch live block
            resp = {}
            counter = 1
            live_block = soup.find_all('section', {"class": "default-match-block"})
            # for line in def_match_block:
            # print line
            for match_block in live_block:
                dic = {}
                match_info = match_block.find_all('span', {"class": "match-no"})[0].text.replace('\n', '').strip()
                team_1 = match_block.find_all('div', {"class": "innings-info-1"})[0].text.replace('\n', '').strip()
                team_2 = match_block.find_all('div', {"class": "innings-info-2"})[0].text.replace('\n', '').strip()
                match_status = match_block.find_all('div', {"class": "match-status"})[0].text.replace('\n', '')
                match_code = str(match_block.find_all('a')[0].get("href")).split('/')[-1].split('.')[0].replace('\n',
                                                                                                                '')
                match_url = str(match_block.find_all('a')[0].get("href"))
                tmp = team_1.split(" ")
                print tmp
                dic["team_1"] = ""
                for t in tmp:
                    try:
                        if t[0].isdigit():
                            break
                    except:
                        pass
                    dic["team_1"] += " " + t
                tmp = team_2.split(" ")
                print tmp
                dic["team_2"] = ""
                for t in tmp:
                    try:
                        if t[0].isdigit():
                            break
                    except:
                        pass
                    dic["team_2"] += " " + t
                # to remove space at 0th index
                # to do : remove trailing spaces

                dic["team_1"] = (dic["team_1"]).strip()
                dic["team_2"]=(dic["team_2"]).strip()

                dic["status"] = match_status
                # dic["code"] = match_code
                dic["info"] = match_info
                dic["url"] = self.url + match_url
                # tmp_json = json.dumps(dic)

                resp[counter] = dic
                counter += 1
            resp = collections.OrderedDict(resp.items())
            return resp
        else:
            print "something went wrong"
            return -1

    def get_match_details(self, match_code):
        matches = self.get_all_games()
        match = matches[match_code]
        team_1 = match['team_1']
        team_2 = match['team_2']
        match_url = match['url']
        resp = requests.get(match_url, headers=self.headers)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            summary = soup.find_all('title')[0].text
            if '(' in summary:
                summary = summary.split('(')
                score = summary[0]
                summary = summary[1].split(')')
                details = summary[0]
                status = match['status']
                result = {'team_1': team_1, 'team_2': team_2, 'score': score, 'details': details, 'status': status}
            else:
                result = {'team_1': team_1, 'team_2': team_2, 'status': 'Game yet to begin'}
            return result
        else:
            print 'Something went wrong :('
            return -1
