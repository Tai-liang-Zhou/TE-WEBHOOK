#!/bin/bash

# - bind on 8000 port
# - sapwn 2 worker process
# - set request timeout as 20 seconds, process not responding for 20 seconds
#   will be restarted automatically.
gunicorn -p gunicorn.pid --bind 0.0.0.0:$TW_PORT --timeout=300 --workers=5 -k gevent server:api
