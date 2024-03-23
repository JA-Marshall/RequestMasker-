from collections import deque
import os
import random
import requests
from fake_useragent import UserAgent

def get_all_proxies_from_webshare():
    proxy_list = []
    next_page = "https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page=1&page_size=25"
    user_agent = UserAgent()
    while next_page:
        response = requests.get(
            next_page,
            headers={"Authorization": os.environ["WEBSHARE_TOKEN"]}
        )
        proxies_data = response.json()

        for index,proxy_data in enumerate(proxies_data["results"]):
            if proxy_data["valid"]:
                proxy_url = f'{proxy_data["username"]}:{proxy_data["password"]}@{proxy_data["proxy_address"]}:{proxy_data["port"]}'
                proxy_and_user_agent = {
                    'id' : index,
                    'http': f'http://{proxy_url}',
                    'https': f'http://{proxy_url}',
                    'user_agent': user_agent.random,
                    'fail_counter'  : 0
                }
                proxy_list.append(proxy_and_user_agent)
        next_page = proxies_data["next"]
    random.shuffle(proxy_list)  # Shuffle to prevent frequent burnout of the first proxies
    return proxy_list

# TODO: Do some validation on the text file
# def get_all_proxies_from_txt():
#     with open("proxies.txt", "r") as file:
#         data = file.readlines()
#     proxy_list = []
#     user_agent = UserAgent()
#     for index,line in enumerate(data):
#         proxy_url = line.strip()
#         proxy_and_user_agent = {
#             'proxy_id' : index,
#             'http': f'http://{proxy_url}',
#             'https': f'https://{proxy_url}',
#             'user_agent': user_agent.random
#         }
#         proxy_list.append(proxy_and_user_agent)
#     return proxy_list

class Proxy_Manager:
    def __init__(self, proxy_list):
        self.proxies = deque(proxy_list)
        self.bad_proxy_dict = {}
        self.failed_request_limit = 50
        
    def get_next_proxy(self):
        if self.proxies:
            next_proxy_and_useragent = self.proxies[0]
            proxy = {key: next_proxy_and_useragent[key] for key in next_proxy_and_useragent if key in ('http', 'https')}
            headers = {'User-Agent': next_proxy_and_useragent['user_agent']}
            #print('rotating')
            self.rotate_proxies()
            print(f'{headers}')
            return proxy, headers
        else:
            print('NO MORE PROXIES LEFT')  # TODO: Add proper exception handling

    def rotate_proxies(self):
        self.proxies.rotate(-1)
        

        
    def report_proxy_error(self):
        bad_proxy = self.proxies[-1]
        bad_proxy['fail_counter'] += 1
        if bad_proxy['fail_counter'] >= self.failed_request_limit:
            self.proxies.pop(-1)
        
        pass
