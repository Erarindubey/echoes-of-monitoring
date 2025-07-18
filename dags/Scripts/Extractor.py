import logging
import requests
import smtplib
from email.mime.text import MIMEText

def send_email_alert(subject, message,to_email):
    msg= MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = 'your email'
    msg['To'] = to_email
    try:
        with smtplib.SMTP('smtp.your-email-provider.com', 587) as server:
            server.starttls()
            server.login('your email', 'your password')
            server.sendmail(msg['From'], [msg['To']], msg.as_string())
        logging.info(f"Email alert sent to {to_email} with subject: {subject}")
    except Exception as e:
        logging.error(f"Failed to send email alert: {e}")

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
def file_extractor_operator(**kwargs):
        import os, shutil, logging
        logging.basicConfig(filename='extractor.log',level=logging.INFO)
        logging.info("File extractor operator started")
        source_dir=kwargs.get("source_dir","/opt/output/streamline2_run")
        if not os.listdir(source_dir):
            logging.warning(f"Source directory {source_dir} is empty. No files to copy.")
            return
        dest_dir=kwargs.get("dest_dir","/opt/output/streamline2_run_copy")
        os.makedirs(dest_dir, exist_ok=True)
        logging.info(f"File extractor starting. Source: {source_dir} | Destination: {dest_dir}")
        for file in os.listdir(source_dir):
            logging.info(f'Scanning files in {source_dir}')
            src_path = os.path.join(source_dir,file)
            dest_path = os.path.join(dest_dir,file)

            try:
                logging.info(f'copying {file} from {src_path} to {dest_path}')
                shutil.copy2(src_path, dest_path)
                logging.info(f"Copied {file}")
                update_metric('files_copied', 1)
            except Exception as e:
                logging.error(f'failed to copy {file}: {e}')
                update_metric('file_copy_errors', 1)
                log_alert(f"Failed to copy {file}: {e}")
                logging.info("Recovery wrapper activated")
                send_email_alert(
                    subject="File Copy Error",
                    message=f"Failed to copy {file} from {src_path} to {dest_path}. Error: {e}, Recovery triggered. please check the Dags for more details.",
                    to_email="email where you want to send the alert"
                )
                handle_recovery_error(file,str(e))
        send_email_alert(
            subject="File Extraction Completed",
            message=f"File extraction completed successfully. Files copied from {source_dir} to {dest_dir}.",
            to_email="email where you want to send the alert"
        )

