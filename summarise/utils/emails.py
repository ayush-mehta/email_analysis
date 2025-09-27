import datetime as dt

class Email:
    def __init__(self, email, password):
        self.email = email
        self.password = password
    
    def _read_email(self, query: str):
        pass

    def query_email_by_timeframe(self, start_time: dt.datetime, end_time: dt.datetime):
        pass
    
    def send_email(self, to, subject, body):
        pass