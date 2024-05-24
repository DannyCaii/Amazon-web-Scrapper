import pandas as pd
from bs4 import BeautifulSoup
from openpyxl import Workbook

import time
import datetime
#Libary to send Emails to self
import smtplib

import csv
import os

import subprocess

import requests
import codecs
from urllib.parse import urlparse  # For filename extraction

site_to_check = [
    # Fresh Produce Apples Bananas Strawberries Avocados Bell Peppers Carrots Broccoli Garlic Lemons/Limes Onion Parsley Cilantro Basil Potatoes Spinach Tomatoes

    'https://www.amazon.com/Organic-Honeycrisp-Apple-One-Medium/dp/B001GIP2A8/ref=sr_1_3_f3_wg?almBrandId=QW1hem9uIEZyZXNo&fpw=alm&s=amazonfresh&sr=1-3',
    'https://www.amazon.com/Dole-Organic-Bananas-Bag/dp/B07ZLF9G83?pd_rd_i=B07ZLF9G83&fpw=alm&almBrandId=QW1hem9uIEZyZXNo&ref_=pd_alm_fs_dsk_sf_ai_16318981_1_1_i',
    'https://www.amazon.com/produce-aisle-Strawberries-1-lb/dp/B000P6J0SM?pd_rd_i=B000P6J0SM&fpw=alm&almBrandId=QW1hem9uIEZyZXNo&ref_=pd_alm_fs_dsk_sf_ai_16318981_1_3_i',
    'https://www.amazon.com/Hass-Avocado-Large-Ready-Eat/dp/B000NOGKN4?pd_rd_i=B000NOGKN4&fpw=alm&almBrandId=QW1hem9uIEZyZXNo&ref_=pd_alm_fs_dsk_sf_ai_16318981_1_5_i',
    'https://www.amazon.com/Fresh-Brand-Stoplight-Bell-Peppers/dp/B086WXFWP4/ref=sr_1_2_f3_wg?almBrandId=QW1hem9uIEZyZXNo&fpw=alm&s=amazonfresh&sr=1-2',
    'https://www.amazon.com/Fresh-Brand-Whole-Carrots-16/dp/B07XLV61C9/ref=sr_1_3_f3_wg?almBrandId=QW1hem9uIEZyZXNo&fpw=alm&s=amazonfresh&sr=1-3',
    'https://www.amazon.com/Church-Brothers-Farms-Broccoli-Florets/dp/B09GWDQZW3/ref=sr_1_5_f3_wg?almBrandId=QW1hem9uIEZyZXNo&fpw=alm&s=amazonfresh&sr=1-5',
    'https://www.amazon.com/Christopher-Ranch-White-Garlic-pack/dp/B09B323RJV/ref=sr_1_1_f3_wg?almBrandId=QW1hem9uIEZyZXNo&fpw=alm&s=amazonfresh&sr=1-1',
    'https://www.amazon.com/produce-aisle-Lemon-One-Medium/dp/B001L1KRNC/ref=sr_1_1_f3_wg?almBrandId=QW1hem9uIEZyZXNo&fpw=alm&s=amazonfresh&sr=1-1',
    'https://www.amazon.com/produce-aisle-mburring-Yellow-Onion/dp/B001W3T2SK/ref=sr_1_1_f3_wg?almBrandId=QW1hem9uIEZyZXNo&fpw=alm&s=amazonfresh&sr=1-1',
    'https://www.amazon.com/Tanimura-Antle-Italian-Parsley-Bunch/dp/B08731FV2H/ref=sr_1_1_f3_wg?almBrandId=QW1hem9uIEZyZXNo&fpw=alm&s=amazonfresh&sr=1-1',
    'https://www.amazon.com/Tanimura-Antle-Cilantro-1-Bunch/dp/B08731HWZV/ref=sr_1_1_f3_wg?almBrandId=QW1hem9uIEZyZXNo&fpw=alm&s=amazonfresh&sr=1-1',
    'https://www.amazon.com/Fresh-Brand-Organic-Basil-0-5/dp/B097F282FC/ref=sr_1_2_f3_wg?almBrandId=QW1hem9uIEZyZXNo&fpw=alm&s=amazonfresh&sr=1-2',
    'https://www.amazon.com/Fresh-Brand-Russet-Potatoes/dp/B07XW1TNXZ/ref=sr_1_1_f3_wg?almBrandId=QW1hem9uIEZyZXNo&fpw=alm&s=amazonfresh&sr=1-1',
    'https://www.amazon.com/Taylor-Farms-65107-Spinach-Bag/dp/B00KMM8I6Y/ref=sr_1_2_f3_wg?almBrandId=QW1hem9uIEZyZXNo&fpw=alm&s=amazonfresh&sr=1-2',
    'https://www.amazon.com/Fresh-Brand-Vine-Tomatoes/dp/B086WX15TH/ref=sr_1_2_f3_wg?almBrandId=QW1hem9uIEZyZXNo&fpw=alm&s=amazonfresh&sr=1-2',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    # '',
    ]

def write_price_data_to_csv(data, filename='amazon_web_scrapper_dataset.csv'):
  """
  Writes price data to a CSV file.

  Args:
      data: List of lists containing product information (title, price, date, link).
      filename: Name of the output CSV file (default: 'amazon_web_scrapper_dataset.csv').
  """
  header = ['Title', 'Price', 'Date', 'Link']

  # Check if file exists and write header if not
  if not os.path.exists(filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
      writer = csv.writer(f)
      writer.writerow(header)

  # Append data to existing file
  with open(filename, 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(data)

  print(f'Data appended to CSV file: {filename}')



def check_price():
    """
    Downloads HTML content, extracts price data, writes to CSV and saves HTML files.
    """
    # Path to the folder for downloaded HTML files
    folder_path = "downloaded_html"

    for url in site_to_check:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
                       'Cache-Control': 'no-cache'}

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                filename = os.path.basename(urlparse(url).path).strip() + '.html'
                full_path_html = os.path.join(folder_path, filename)

                # Downloaded content
                html_content = response.text

                # Process the HTML content
                soup = BeautifulSoup(html_content, 'html.parser')

                # Access and process the parsed HTML using BeautifulSoup methods
                title = soup.find(id='productTitle').text.strip()
                price = soup.find(class_='a-price-whole').text.strip() + soup.find(class_='a-price-fraction').text.strip()
                today = datetime.date.today()  # Import date if not already imported

                link = url

                print(f"Processing price data from {url}")

                # Write HTML content
                with codecs.open(full_path_html, 'w', encoding='utf-8') as f:
                    f.write(html_content)

                # Write price data to CSV
                data = [[title, price, today, link]]
                write_price_data_to_csv(data)

            else:
                print(f'Failed to download {url} (Status code: {response.status_code})')
        except Exception as e:
            print(f"Error processing {url}: {e}")

check_price()