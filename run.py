from usps import download_files
from sendemail import send_mail
import os

files = download_files()
if files:
    send_mail(files)

    for f in files:
        os.remove(f)
