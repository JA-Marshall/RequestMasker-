# RequestMasker

RequestMasker is a Python library designed to allow for me to more efficiently use proxies i was buying from webshare, they had a "rotating proxy" you could call but i wanted to manage them myself and rotate them in and out more efficiently
This is a WIP as it was pulled out of another project but i want to turn this into a full usable library/framework

## Key Features

- **Proxy Rotation**: Seamlessly integrates with Webshare for fresh proxies and supports custom proxy lists, enabling extensive rotation to avoid bans and rate-limiting.
- **Dynamic User-Agent**: Each proxy is assigend a unique useragent so that every request from that IP has a matching agent.
- **Concurrent Request Handling**: Utilizes threading to manage multiple requests simultaneously, significantly improving the throughput of your data collection or scraping operations.


## Getting Started
WIP


### Installation

git clone https://github.com/JA-Marshall/RequestMasker-.git
cd requestmasker
pip install -r requirements.txt
