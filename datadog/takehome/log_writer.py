#! /usr/bin/env python3

import datetime
import random
import time


def main(filename):
    bufsize = 1
    with open(filename, 'a', bufsize) as f:
        while True:
            user_ids = ['james', 'jill', 'frank', 'mary']
            user_id = random.choice(user_ids)
            dt = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S %Z').strip()
            methods = ['GET', 'PUT', 'POST', 'DELETE']
            method = random.choice(methods)
            requests = [
                '/report',
                '/api/users',
                '/api/stats',
            ]
            request = random.choice(requests)

            size = random.randrange(1, 1000000)
            logline = """{client} - {user_id} [{dt}] "{method} {request} {protocol}" {status_code} {size}\n""".format(
                client='127.0.0.1',
                user_id=user_id,
                dt=dt,
                method=method,
                request=request,
                protocol='HTTP/1.0',
                status_code=200,
                size=size)
            print(logline.strip())

            f.write(logline)
            time.sleep(1)


if __name__ == "__main__":
    try:
        filename = 'access.log'
        main('access.log')
    except KeyboardInterrupt:
        pass
