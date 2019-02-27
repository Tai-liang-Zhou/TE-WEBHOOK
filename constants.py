# -*- coding: utf-8 -*-
import os

# name of environment variables
# SYSTEX_URL = os.environ.get('TW_SYSTEX_URL', 'http://booking.eastus.cloudapp.azure.com:8080/VBooking/rest/')
SYSTEX_URL = os.environ.get('TW_SYSTEX_URL', 'http://vbooking.eastasia.cloudapp.azure.com:8080/VBooking/rest/')
COMMON_PARSER_SERVICE_URL = os.environ.get('TW_COMMON_PARSER_SERVICE_URL', 'http://dev1.emotibot.com:14901/common-parser-service')
TDE_URL = os.environ.get('TDE_URL', 'http://poc2.emotibot.com:10999/tde/usp/parse')
REQUEST_TIMEOUT = os.environ.get('TW_REQUEST_TIMEOUT', '4')