from flask import Flask, request
from prometheus_client import Gauge, start_http_server
import threading
import logging
import time

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger('metrics')

files_copied = Gauge('files_copied', 'Total number of files successfully copied')
copy_errors = Gauge('file_copy_errors', 'Total number of file copy errors')

@app.route('/update', methods=['POST'])
def update_metrics():
    data = request.json
    if 'files_copied' in data:
        files_copied.inc(data['files_copied'])
    if 'file_copy_errors' in data:
        copy_errors.inc(data['file_copy_errors'])
    return "Metrics updated", 200

def start_flask():
    app.run(host="0.0.0.0", port=9200)

if __name__ == "__main__":
    start_http_server(9100)
    threading.Thread(target=start_flask).start()

    while True:
        time.sleep(10)