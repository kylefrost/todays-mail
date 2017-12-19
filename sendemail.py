from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.utils import formataddr
from email.header import Header
from os.path import basename
from datetime import date
import smtplib
import config
import sys
import os

def send_mail(files=None):
    thisPath = os.path.split(os.path.abspath(sys.argv[0]))[0] + "/"

    with open(thisPath + 'email.html', 'r') as htmlFile:
        HTML = htmlFile.read()

    with open(thisPath + 'email.css', 'r') as cssFile:
        CSS = cssFile.read()

    HTML = HTML.replace('{{ emailcss }}', CSS)
    HTML = HTML.replace('{{ emailheader }}', config.HEADER)
    HTML = HTML.replace('{{ emailfooter }}', config.FOOTER)

    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = config.SUBJECT
    msgRoot['From'] = formataddr((str(Header(config.FROM_NAME, 'utf-8')), config.FROM_EMAIL))
    msgRoot['To'] = ','.join(config.TO_EMAILS)

    msgAlt = MIMEMultipart('alternative')
    msgRoot.attach(msgAlt)

    bodyTxt = MIMEText('Your email client does not support HTML messages.')
    msgAlt.attach(bodyTxt)

    td_temp = """
    <tr>
        <td><img src="{{ image }}"></td>
    </tr>
    """

    imagetable = ''

    for f in files or []:
        imagetable = imagetable + td_temp.replace("{{ image }}", "cid:%s" % (basename(f)))

    HTML = HTML.replace('{{ imagetable }}', imagetable)
    HTML = HTML.replace('{{ mailcount }}', str(len(files)) + (' pieces' if len(files) > 1 else ' piece'))
    HTML = HTML.replace('{{ emaildate }}', date.today().strftime('%A, %B %-d, %Y'))

    bodyHtml = MIMEText(HTML, 'html')
    msgAlt.attach(bodyHtml)

    for f in files or []:
        fp = open(f, 'rb')
        msgImg = MIMEImage(fp.read())
        fp.close()
        msgImg.add_header('Content-ID', '<{}>'.format(basename(f)))
        msgRoot.attach(msgImg)

    server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
    server.starttls()
    server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
    server.sendmail(config.FROM_EMAIL, config.TO_EMAILS, msgRoot.as_string())
    server.quit()
