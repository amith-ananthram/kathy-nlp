import sys
import traceback
from datetime import datetime
from subprocess import Popen, PIPE
from email.mime.text import MIMEText
from contextlib import contextmanager
from dateutil.relativedelta import relativedelta

ATTRS = ['years', 'months', 'days', 'hours', 'minutes', 'seconds']

def elapsed_time(t1, t2):
	delta = relativedelta(t2, t1)
	return ', '.join(
		['%d %s' % (getattr(delta, attr), attr if getattr(delta, attr) > 1 else attr[:-1]) 
			for attr in ATTRS if getattr(delta, attr)]
	)


def email(to_email, subj, body):
	msg = MIMEText(body)
	msg["To"] = to_email
	msg["Subject"] = subj
	p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
	p.communicate(msg.as_bytes() if sys.version_info >= (3,0) else msg.as_string()) 


@contextmanager
def monitored(variant, to_email, report_success):
	start = datetime.now()
	try:
		yield
	except Exception as e:
		end = datetime.now()
		subj = f"{variant} failed!"
		body = f"{variant} failed after {elapsed_time(start, end)}!  Error:\n\n{traceback.format_exc()}"
		email(to_email, subj, body)
		raise e
	
	if report_success:
		end = datetime.now()
		subj = f"{variant} succeeded!"
		body = f"{variant} succeeded after {elapsed_time(start, end)}!"
		email(to_email, subj, body)
