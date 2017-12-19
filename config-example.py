"""

Config file for todays-mail


"""

# Bold text at the top of the email
HEADER = 'Today\'s Mail'

# Small text at the bottom of the email
FOOTER = 'Automated Mail System'

# Subject of the email
SUBJECT = 'Today\'s Mail'

# Your my.usps.com Login Information
MYUSPS_USERNAME = ''
MYUSPS_PASSWORD = ''

# Who the email will show as From
FROM_NAME = 'Automated Mail System'
FROM_EMAIL = 'no_reply@example.com'

# Who you want the mail email sent to as a list
TO_EMAILS = ['example@example.com', 'example2@example.com']

# SMTP Outgoing mail information
SMTP_USERNAME = ''
SMTP_PASSWORD = ''
SMTP_SERVER = ''
SMTP_PORT = 587
