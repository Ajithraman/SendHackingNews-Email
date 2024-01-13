import requests as re
from bs4 import BeautifulSoup
import pandas as pd
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

url = "https://thehackernews.com/"
data = re.get(url)

# Delete the file if exists
if os.path.exists('output.csv'):
    os.remove('output.csv')

if os.path.exists('headline.txt'):
    os.remove('headline.txt')

if os.path.exists('link.txt'):
    os.remove('link.txt')
if os.path.exists('final.html'):
    os.remove('final.html')
if os.path.exists('combined_data.csv'):
    os.remove('combined_data.csv')

soup = BeautifulSoup(data.content,"html.parser")
head = soup.find_all("div", class_="clear home-right")

# Grabbing headlines
for headline in head:
  result = headline.h2.text
  with open('headline.txt', 'a') as file:
    file.write(result + "\n")

head_link = soup.find_all("a", class_="story-link")


# Grabbing links
for header in head_link:
  link = header["href"]
  with open('link.txt', 'a') as file:
    file.write(link + "\n")

with open('headline.txt', 'r') as file:
    headlines = file.readlines()

with open('link.txt', 'r') as file:
    links = file.readlines()

# Create a DataFrame
df = pd.DataFrame({'Headline': headlines, 'Link': links})

# Remove newline characters from the columns
df['Headline'] = df['Headline'].str.strip()
df['Link'] = df['Link'].str.strip()

# Save the DataFrame to a CSV file
df.to_csv('combined_data.csv', index=False)

demo = pd.read_csv('combined_data.csv')

html_table = df.style.set_table_styles([
    {'selector': 'thead th', 'props': [('text-align', 'center')]}
])
# Convert the DataFrame to an HTML table
html_table = demo.to_html(index=False)

# Save the HTML table to a file or print it
with open('final.html', 'w') as file:
    file.write(html_table)

sender_email = ""  # Sender's email address
receiver_email = ""  # Recipient's email address
subject = "Today News"

# Set up the MIME object
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = subject

# Attach the HTML table to the email
body = MIMEText(html_table, 'html')
message.attach(body)

# Create an SMTP session and send the email
with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
    server.login(sender_email, "")   # sender gmail app password 
    server.sendmail(sender_email, receiver_email, message.as_string())

print("Email sent successfully.")
