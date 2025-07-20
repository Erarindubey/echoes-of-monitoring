from pyspark.sql import SparkSession
import logging
import requests
import os
import time
import smtplib
from email.mime.text import MIMEText

def send_email(subject, message, to_email):
    msg= MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = 'your_email'
    msg['To'] = to_email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('your_email','pass')
            server.send_message(msg)
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

def update_metric(metric_name, value):
    try:
        response = requests.post("http://metrics_server:9200/update", json={metric_name: value})
        if response.status_code == 200:
            logging.info(f"Metric '{metric_name}' updated with value: {value}")
        else:
            logging.warning(f"Failed to update metric '{metric_name}': {response.status_code}")
    except Exception as e:
        logging.error(f"Error while sending metric '{metric_name}': {e}")
def log_alert(message):
    logging.warning(message)
def recovery_wrapper(func):
    def wrapper(*args, **kwargs):
        try:
            logging.info("Recovery wrapper activated")
            logging.info(f"Calling function: {func.__name__} with args: {kwargs}")
            return func(*args, **kwargs)
        except FileNotFoundError:
            log_alert("Source file is missing. Skipping and alerting...")
            update_metric('file_copy_errors', 1)
        except Exception as e:
            log_alert(f"Unhandled error: {e}")
            update_metric('file_copy_errors', 1)
            raise e
    return wrapper
def handle_recovery_error(file, error_msg):
    log_alert(f"Recovery triggered for {file}: {error_msg}")
@recovery_wrapper
def heartbeat(**kwargs):
    logging.info("Hybrid DAG heartbeat triggered.")
    update_metric('dag_heartbeat', 1)
def streamlinepipline4(**kwargs):
    log_path=r"/opt/logs/streamline.log"
    if not os.access(log_path, os.W_OK):
        log_path=r'/tmp/streamline.log'
    logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler()
        ]
    )
    logging.info("Streamline pipeline 4 started")
    update_metric('pipeline_start_time', time.time())
    log = logging.getLogger("streamline")
    sp=SparkSession.builder.appName('Streamline pipeline 4').getOrCreate()
    local_dir=kwargs.get("local_dir", "/opt/input")
    output_dir=kwargs.get("output_dir", "/opt/output/streamline2_run")
    csv_files=[f for f in os.listdir(local_dir) if f.endswith('.csv')]
    st1=time.time()
    for name in csv_files:
        try:
            st2 = time.time()
            df=sp.read.format('csv').option('inferSchema','True').option('header','True').option('delimiter',',').load(fr'{local_dir}/{name}')
            df.repartition(6).write.mode('overwrite').parquet(output_dir)
            update_metric('files_copied', 1)
            log.info(f"{name} processed -> Time taken: {round(time.time() - st2, 2)} sec")
            update_metric(f"{name}_processing_time_sec", round(time.time() - st2, 2))
            del df
        except Exception as e:
            handle_recovery_error(name, str(e))
            update_metric('file_copy_errors', 1)
    et=time.time()
    print(f'Total Time:- {round(et-st1,2)}')
    log.info(f"{len(csv_files)} files processed. Output written to: {output_dir}")
    send_email('ETL Status',f'file processing completed successfully. Total time taken: {round(et-st1,2)} seconds','to_email')
    update_metric('pipeline_end_time', time.time())
    sp.stop()