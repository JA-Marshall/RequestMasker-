# RequestMasker

RequestMasker is a Python library designed to allow for me to more efficiently use proxies i was buying from webshare, they had a "rotating proxy" you could call but i wanted to manage them myself and rotate them in and out more efficiently
This is a WIP as it was pulled out of another project but i want to turn this into a full usable library/framework

## Key Features

- **Proxy Rotation**: Seamlessly integrates with Webshare for fresh proxies and supports custom proxy lists, enabling extensive rotation to avoid bans and rate-limiting.
- **Dynamic User-Agent**: Each proxy is assigend a unique useragent so that every request from that IP has a matching agent.
- **Concurrent Request Handling**: Utilizes threading to manage multiple requests simultaneously, significantly improving the throughput of your data collection or scraping operations.

![image](https://github.com/JA-Marshall/RequestMasker-/assets/9871373/017917fb-0d9e-4586-9380-22c6bfaed540)
- using the test server and the example in the testing branch i was able to send 1000 requests to my own server from 250 different proxies in 2-3 seconds.
- don't actually do that to other peoples servers, i originally wrote this because the site i was scraping had a 20 second cooldown between scraping and i wanted to fully optimize proxy usage.

- 
## Getting Started
WIP


### Installation

git clone https://github.com/JA-Marshall/RequestMasker-.git
cd requestmasker
pip install -r requirements.txt
