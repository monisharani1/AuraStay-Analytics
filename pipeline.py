import pandas as pd
import boto3
from sqlalchemy import create_engine
import urllib.parse

# --- 1. AWS SETUP ---
# PUT YOUR ACTUAL KEYS HERE
AWS_ACCESS_KEY = 'YOUR_ACCESS_KEY_HERE'
AWS_SECRET_KEY = 'YOUR_SECRET_KEY_HERE'
BUCKET_NAME = 'monisha-hotel-booking-2026'
FILE_NAME = 'hotel_bookings.csv' 

print("Connecting to AWS S3...")
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

# --- 2. DOWNLOAD DATA ---
print("Downloading data from S3...")
obj = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_NAME)
df = pd.read_csv(obj['Body'])

# --- 3. CLEAN DATA ---
print("Cleaning data...")
# Drop rows where the price (adr) is missing
df = df.dropna(subset=['adr'])
# Calculate total revenue (Price * Total nights)
df['total_nights'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
df['revenue'] = df['adr'] * df['total_nights']

# --- 4. PUSH TO MYSQL ---
print("Saving to MySQL Database...")
# PUT YOUR ACTUAL MYSQL PASSWORD HERE
MYSQL_PASSWORD = 'monalisa'

# We use urllib to safely encode your password in case it has special characters like @ or #
encoded_password = urllib.parse.quote_plus(MYSQL_PASSWORD)

# Connect to the database
engine = create_engine(f'mysql+mysqlconnector://root:{encoded_password}@localhost/hotel_db')

# Push the data
df.to_sql('bookings', con=engine, if_exists='replace', index=False)
print("Success! Data is in MySQL.")