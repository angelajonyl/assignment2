# COSC 1104 - Assignment2
# Author: Angela Reyes

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Constants
URL = "https://www.maine.gov/agviewer/content/ag/985235c7-cb95-4be2-8792-a1252b4f8318/list.html"
ADMIN_EMAIL = "samp.notifcation@gmail.com"  # Admin's email
SMTP_SERVER = "smtp.gmail.com"  
SMTP_PORT = 587
EMAIL_USER = "samp.notifcation@gmail.com"  # 
EMAIL_PASS = "vlip iqth uyqz pspo"  # App Password

def fetch_breach_data():
    """Fetches breach data from the Maine AG website."""
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Locate the table containing breach data
    table = soup.find("table")
    if not table:
        raise ValueError("No table found on the webpage.")
    
    rows = table.find_all("tr")[1:]  # Skips the table header
    breaches = []
    
    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 2:
            date_reported = cells[0].text.strip()
            org_name = cells[1].text.strip()
            breaches.append((date_reported, org_name))
    return breaches

def filter_breaches_by_date(breaches, target_date):
    """Filters breaches reported on the target date."""
    filtered_breaches = []
    for date_reported, org_name in breaches:
        try:
            reported_date = datetime.strptime(date_reported, "%Y-%m-%d")  # Format as needed
            if reported_date.date() == target_date:
                filtered_breaches.append((org_name, date_reported))
        except ValueError:
            print(f"Skipping invalid date format: {date_reported}")  # Debugging
    return filtered_breaches

def send_email(subject, body):
    """Sends an email to the admin."""
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = ADMIN_EMAIL
    msg["Subject"] = subject
    
    msg.attach(MIMEText(body, "plain"))
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

def main():
    yesterday = (datetime.utcnow() - timedelta(days=1)).date()  # UTC for consistency
    breaches = fetch_breach_data()
    yesterdays_breaches = filter_breaches_by_date(breaches, yesterday)
    
    if yesterdays_breaches:
        subject = f"Breach Notifications Reported on {yesterday}"
        body = "The following organizations reported breaches yesterday:\n\n"
        body += "\n".join(f"- {org_name} (Reported: {date})" for org_name, date in yesterdays_breaches)
        body += f"\n\nSource: {URL}"
        send_email(subject, body)
        print("Notification sent!")
    else:
        print("No breaches reported yesterday.")

if __name__ == "__main__":
    main()
