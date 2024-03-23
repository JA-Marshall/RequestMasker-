from flask import Flask, request
import time

app = Flask(__name__)
request_counter = 0
start_time = time.time()
unique_user_agent_pairs = set() 

@app.route('/')
def home():
    global request_counter
    global start_time
    request_counter += 1
    print(request_counter)
    if request_counter == 0:
        start_time = time.time()
    
    user_agent = request.headers.get('User-Agent')
    # Getting the IP address; 'X-Forwarded-For' is for proxies, while 'remote_addr' is for direct connections.
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    pair = (ip_address, user_agent)
    if pair not in unique_user_agent_pairs:
        unique_user_agent_pairs.add(pair)
    if request_counter >= 1000:
        end_time = time.time()
        total_time = end_time - start_time

        print(f"\n\n\n {request_counter} requests received in {round(total_time, 2)} seconds")
        print(f'{len(unique_user_agent_pairs)} unique ips')
        print(unique_user_agent_pairs)

        # Shutdown the server
   
        return "stop"

    return "Hello, World!"


if __name__ == '__main__':
    app.run()
