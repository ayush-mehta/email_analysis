import datetime as dt
import imaplib
import email
import base64
from email.header import decode_header
from typing import Any, Dict, List


class Email:
    def __init__(self, email, password, imap_server) -> None:
        self.email: str = email
        self.password: str = password
        self.imap_server: str = imap_server
        self.mail: imaplib.IMAP4_SSL = imaplib.IMAP4_SSL(self.imap_server)

    def login(self) -> None:
        self.mail.login(self.email, self.password)
        self.mail.select("INBOX")

    def logout(self) -> None:
        self.mail.close()
        self.mail.logout()

    def query_email_by_timeframe(
        self,
        start_time: dt.datetime,
        end_time: dt.datetime,
        download_attachments: bool = False,
    ):
        start_date_str = start_time.strftime("%d-%b-%Y")
        end_date_str = end_time.strftime("%d-%b-%Y")

        query = f'SINCE "{start_date_str}" BEFORE "{end_date_str}"'
        messages = self._query_email(query)

        emails = self._fetch_and_parse_email(
            messages=messages, download_attachments=download_attachments
        )
        return emails

    def send_email(self, to, subject, body):
        pass

    def _query_email(self, query: str) -> List[str]:
        status, messages = self.mail.search(None, query)
        if status != "OK":
            raise Exception(f"Error searching emails: {messages}")
        return messages

    def _fetch_and_parse_email(
        self, messages: List[str], download_attachments: bool = False
    ) -> List[Dict[str, Any]]:
        email_identifiers = messages[0].split()
        emails = []
        for email_identifier in email_identifiers:
            try:
                status, msg_data = self.mail.fetch(email_identifier, "(RFC822)")

                if status != "OK":
                    raise Exception(
                        f"Error fetching email_identifier {email_identifier} info: {msg_data}"
                    )

                raw_email = msg_data[0][1]
                email_message = email.message_from_bytes(raw_email)

                subject = self._decode_header(email_message.get("Subject", ""))
                from_addr = self._decode_header(email_message.get("From", ""))
                to_addr = self._decode_header(email_message.get("To", ""))
                cc_addr = self._decode_header(email_message.get("Cc", ""))
                reply_to = self._decode_header(email_message.get("Reply-To", ""))
                date = email_message.get("Date", "")

                message_id = email_message.get("Message-ID", "")
                in_reply_to = email_message.get("In-Reply-To", "")
                references = email_message.get("References", "")

                body = self._extract_body(email_message)
                attachments = self._extract_attachments(
                    email_message=email_message,
                    download_attachments=download_attachments,
                )

                emails.append(
                    {
                        "subject": subject,
                        "from": from_addr,
                        "to": to_addr,
                        "cc": cc_addr,
                        "reply_to": reply_to,
                        "date": date,
                        "body": body,
                        "thread": {
                            "message_id": message_id,
                            "in_reply_to": in_reply_to,
                            "references": references,
                        },
                        "attachments": attachments,
                    }
                )

            except Exception as e:
                print(f"Error in fetching and parsing emails of {self.email}: {str(e)}")
                continue
        return emails

    def _decode_header(self, header_value):
        if not header_value:
            return ""

        decoded_parts = decode_header(header_value)
        decoded_string = ""

        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                if encoding:
                    decoded_string += part.decode(encoding)
                else:
                    decoded_string += part.decode("utf-8", errors="ignore")
            else:
                decoded_string += part

        return decoded_string

    def _extract_body(self, email_message):
        body = ""

        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition", ""))

                if "attachment" in content_disposition:
                    continue

                if content_type == "text/plain":
                    try:
                        body += part.get_payload(decode=True).decode(
                            "utf-8", errors="ignore"
                        )
                    except:
                        pass
                elif content_type == "text/html" and not body:
                    try:
                        body += part.get_payload(decode=True).decode(
                            "utf-8", errors="ignore"
                        )
                    except:
                        pass
        else:
            content_type = email_message.get_content_type()
            if content_type in ["text/plain", "text/html"]:
                try:
                    body = email_message.get_payload(decode=True).decode(
                        "utf-8", errors="ignore"
                    )
                except:
                    pass

        return body.strip()

    def _extract_attachments(self, email_message, download_attachments: bool = False):
        attachments = []

        if email_message.is_multipart():
            for part in email_message.walk():
                content_disposition = str(part.get("Content-Disposition", ""))
                content_type = part.get_content_type()

                if "attachment" in content_disposition or (
                    content_disposition == "" and part.get_filename()
                ):
                    filename = part.get_filename()
                    if filename:
                        filename = self._decode_header(filename)
                        if download_attachments:
                            file_content = part.get_payload(decode=True)
                        else:
                            file_content = None

                        file_size = len(file_content) if file_content else 0

                        content_type = part.get_content_type()

                        attachments.append(
                            {
                                "filename": filename,
                                "content_type": content_type,
                                "size": file_size,
                                "content_disposition": content_disposition,
                                "content": file_content,
                                "content_base64": (
                                    self._encode_base64(file_content)
                                    if file_content
                                    else None
                                ),
                            }
                        )

        return attachments

    def _encode_base64(self, data):
        return base64.b64encode(data).decode("utf-8")
