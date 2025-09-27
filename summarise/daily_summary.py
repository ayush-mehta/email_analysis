from config import config
from utils.emails import Email
import datetime as dt

def main(event, context):
    email_ids = event.get('email_ids', [])
    email_configs = config['read_email_credentials']
    for email_id in email_ids:
        if email_id not in email_configs:
            raise ValueError(f"Email ID {email_id} not found in config.json")
        
        email_obj = Email(
            email=email_id,
            password=email_configs[email_id]['password'],
            imap_server=email_configs[email_id]['imap_server']
        )
        email_obj.login()
        daily_emails = email_obj.query_email_by_timeframe(start_time=dt.datetime.now() - dt.timedelta(days=1), end_time=dt.datetime.now(), download_attachments=True)
        email_obj.logout()
    return {
        'statusCode': 200,
        'body': daily_emails
    }

if __name__ == "__main__":
    # For local testing, call main with dummy event and context
    result = main(event={"email_ids": ["ayushmehta2001108@gmail.com"]}, context={})
    print(result)