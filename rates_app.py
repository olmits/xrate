from flask import Flask
from logging_func import create_logger

app = Flask(__name__)

log = create_logger('main.log')

log.debug('App created')

# import urls
