#####unfinished cleaning up the code as i pulled it from an existing project
#####the only code that changes will be anything inside the main function,



import requests
from fake_useragent import UserAgent
import os
import threading
import proxies
from collections import deque
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
import time

# TODO: Need to move this to some sort of config file
thread_count = 60
max_request_retries = 5




def main(ip):
    list_of_ips = [ip for _ in range(1000)]
    print(len(list_of_ips))
    worker_url_list_of_lists = build_url_sublists(list_of_ips)
    proxy_list = proxies.get_all_proxies_from_webshare()
    worker_proxy_list_of_lists = split_into_chunks(proxy_list)
    start_threads(worker_url_list_of_lists, worker_proxy_list_of_lists)

def start_threads(worker_url_list_of_lists, worker_proxy_list_of_lists):
    threads = []
    for i in range(thread_count):
        worker_url_list = worker_url_list_of_lists[i]
        worker_proxy_list = worker_proxy_list_of_lists[i]

        thread = threading.Thread(target=worker, args=(worker_url_list, worker_proxy_list))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def worker(worker_url_queue, worker_proxy_list):
    proxy_manager = proxies.Proxy_Manager(worker_proxy_list)
    #ugly hack to stop it sending requests once we hit close to 1000
    for url in worker_url_queue:
        proxy, headers = proxy_manager.get_next_proxy()
        #print(proxy,headers)
        retries = 0
        while retries < max_request_retries:
            if retries == 2:
                proxy, headers = proxy_manager.get_next_proxy()

     
            #print(retries)
            response = make_request(url, proxy, headers)
            if response is None:
                print('error, retrying')
                time.sleep(1)
                proxy_manager.report_proxy_error()
                retries += 1
                proxy_manager.rotate_proxies()
            else:
               
                process_response(response)
                
                break

# TODO: Implement proper logging

def make_request(url, proxy, headers):
    try:
        response = requests.get(url, proxies=proxy, headers=headers, timeout=5)
       
        response.raise_for_status()
        return response
    except HTTPError as http_err:
        
        print(f'HTTP error occurred: {http_err} - Status code: {http_err.response.status_code}')
       
    except ConnectionError:
        print('Connection error occurred. The request could not be sent.')

    except Timeout:
        print('The request timed out.')
        
    except RequestException as err:
        print(f'An error occurred: {err}')
      
    return None

def process_response(response):
    # Code for handling the actual response we get would be implemented here,
    #scraping logic for beautifulsoup or parsing JSON from an api etc 

    if 'stop' in response.content.decode('utf-8'):

        #print(response.content)
        stop_event.set()
    
    


def build_url_sublists(product_names):
    url_list = []
    for product in product_names:
        url = product
        url_list.append(url)
    return split_into_chunks(url_list)

def split_into_chunks(full_list, chunk_count=thread_count):
    chunk_size = len(full_list) // chunk_count
    remainder = len(full_list) % chunk_count

    chunks = []
    for i in range(chunk_count):
        start = i * chunk_size + min(i, remainder)
        end = start + chunk_size + (1 if i < remainder else 0)
        chunks.append(full_list[start:end])
    return chunks

if __name__ == '__main__':
    main('http://139.162.200.140:5000')