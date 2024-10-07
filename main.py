import smtplib
import time
import schedule
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Placeholder for LLM function
def ask_llm(prompt):
    # Replace this with your actual LLM integration
    return "This is a placeholder response from the LLM."

class EmailCampaign:
    def init(self, sender_email, sender_password):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipients = []
        self.initial_message = ""
        self.follow_up_messages = []
        self.follow_up_intervals = []

    def add_recipient(self, email, name):
        self.recipients.append({"email": email, "name": name})

    def set_initial_message(self, subject, body):
        self.initial_message = {"subject": subject, "body": body}

    def add_follow_up(self, subject, body, days_after):
        self.follow_up_messages.append({"subject": subject, "body": body})
        self.follow_up_intervals.append(days_after)

    def send_email(self, to_email, subject, body):
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP('smtp.mail.yahoo.com', 587) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            print(f"Email sent successfully to {to_email}")
        except Exception as e:
            print(f"Error sending email to {to_email}: {str(e)}")

    def send_initial_emails(self):
        for recipient in self.recipients:
            self.send_email(recipient['email'], self.initial_message['subject'], self.initial_message['body'])

    def schedule_follow_ups(self):
        for i, follow_up in enumerate(self.follow_up_messages):
            days = sum(self.follow_up_intervals[:i+1])
            schedule.every(days).days.do(self.send_follow_up, i)

    def send_follow_up(self, follow_up_index):
        follow_up = self.follow_up_messages[follow_up_index]
        for recipient in self.recipients:
            self.send_email(recipient['email'], follow_up['subject'], follow_up['body'])

    def run_campaign(self):
        self.send_initial_emails()
        self.schedule_follow_ups()
        
        while True:
            schedule.run_pending()
            self.check_responses()
            time.sleep(60)  # Check every minute

if __name__ == "__main__":
    campaign = EmailCampaign("your_email@yahoo.com", "your_password")

    # Add recipients
    campaign.add_recipient("recipient1@example.com", "John")
    campaign.add_recipient("recipient2@example.com", "Jane")

    # Set initial message
    campaign.set_initial_message(
        "Exciting Opportunity",
        "Dear {name},\n\nI hope this email finds you well. I wanted to reach out about anexciting opportunity..." 
    )

    # Add follow-ups
    campaign.add_follow_up(
        "Following up on our previous email",
        "Dear {name},\n\nI hope you had a chance to review my previous email...",
        3  # Send after 3 days
    )
    campaign.add_follow_up(
        "One last attempt to connect",
        "Dear {name},\n\nI understand you must be busy, but I wanted to make one last attempt...",
        7  # Send 7 days after the first follow-up
    )

    # Run the campaign
    campaign.run_campaign()