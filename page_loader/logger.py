import logging
import sys

logging.basicConfig(filemode='w',
                    datefmt='%d-%b-%y %H:%M:%S',
                    filename='page_loader.log',
                    format='[%(asctime)s] %(module)s - %(levelname)s - %(message)s',
                    )
logger = logging.getLogger()

console_handler = logging.StreamHandler(sys.stderr)
console_handler.setLevel(logging.WARNING)
logger.addHandler(console_handler)
