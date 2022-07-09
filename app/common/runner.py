import re
from subnet.models import Ip
from .models import Description, NetworkConnDescription, Config
from environment.models import Environment
from watcher.models import Watcher

import socket
import errno

import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sync_ip_description():
    descriptions = Description.objects.all()
    ip = Ip.objects.all()
    for ip_obj in ip.iterator():
        for desc in descriptions.iterator():
            if re.search(desc.regex, ip_obj.dns):
                ip_obj.description.add(desc)
        ip_obj.save()

def sync_environment_count():
    environments = Environment.objects.all()
    for env in environments.iterator():
        ip_count = Ip.objects.filter(description=env.regex)
        env.count = len(ip_count)
        env.save()

def check_watcher_status():
    watchers = Watcher.objects.all()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for watcher in watchers:
        try:
            code = sock.connect_ex((watcher.dns, int(watcher.port)))
            error_code = NetworkConnDescription.objects.get(code=code)

            if code == 0:
                watcher.status = 1
                watcher.error_code = error_code
                watcher.save()
                continue
            else:
                watcher.status = 0
                watcher.error_code = error_code
                watcher.save()
        except Exception as e:
            code = 1001
            watcher.error_code = NetworkConnDescription.objects.get(code=code)
            watcher.status = 0
            watcher.save()
            continue

def send_machine_status_alarm():
    config = Config.objects.get(id=1)
    watcher = Watcher.objects.filter(status=0)

    if not config.smtp_enabled or not len(watcher):
        return

    sender = config.smtp_sender
    receivers = _get_receiver_from_config(config)
    html = _machine_status_html(watcher)
    subject = config.smtp_subject

    email_message = MIMEMultipart()
    email_message['From'] = sender
    email_message['To'] = ", ".join(receivers)
    email_message['Subject'] = subject

    email_message.attach(MIMEText(html, "html"))
    # Convert it as a string
    email_string = email_message.as_string()

    context = ssl.create_default_context()

    try:
       smtpObj = smtplib.SMTP(config.smtp_uri, config.smtp_port)
       smtpObj.sendmail(sender, receivers, email_string)         
       print("Successfully sent email")
    except Exception as e:
        print(e)
        print("Error: unable to send email")
        

def check_machine_connection(dns, port):
    status = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.settimeout(2)
    try:
        code = sock.connect_ex((dns, port))
    except socket.gaierror:
        return 1001, 0
    if code == 0:
        status = 1
    sock.close()
    return code, status

def _get_receiver_from_config(config):
    result = []
    for i in config.smtp_receiver.split(","):
        result.append(i.strip())
    return result

def _machine_status_html(watcher):
    tr = ""
    for watch in watcher:
        tr = tr + "<tr><td>"+watch.dns+"</td><td>"+str(watch.port)+"</td></tr>"
    temp = """
    <!DOCTYPE html>
    <html>
    <head>
    <title>Down Machines</title>
    </head>
    <style>
    table {
      border-collapse: collapse;
      width: 100%;
    }

    td, th {
      border: 1px solid #dddddd;
      text-align: center;
      padding:6px 20px;
    }
    tr th {
     border: 1px solid #dddddd;
      text-align: center;
      padding:6px 20px;
      background-color: #ad1e23;
      color:#fff;
    }

    tr:hover {
      background-color: #dddddd;
      cursor: pointer;
    }

    .content td, .content th {
        border-top: 1px solid transparent;
        padding: 2px 10px 2px 15px;
    }
    </style>
    <body>
        <table>
            <tbody>
                <tr>
                    <th colspan="2"><strong>Machine Down Status</strong></th>
                </tr>
                <tr>
                    <th>DNS</th>
                    <th>PORT</th>
                </tr>
                """+tr+"""

            </tbody>
        </table>
    </body>

    </html>


    """
    return temp