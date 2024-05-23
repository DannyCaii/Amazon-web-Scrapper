import time
import datetime
#Libary to send Emails to self
import smtplib

import csv
import pandas as pd
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


# sorted_sites = sorted(site_to_check)

def write_html_file(site, proxy=None, folder_path='downloaded_html', prettify=False):
    try:
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Extract filename between 2nd and 3rd backslashes (consider potential naming issues with special characters)
        url_parts = urlparse(site).path.split('/')
        if len(url_parts) >= 2:  # Ensure there are at least 2 parts (1 backslash)
            filename = f"{url_parts[1]}.html"
        else:
            filename = f"unknown_{site.split('/')[-1]}.html"  # Fallback for malformed URLs

        print(f'Downloading content for {site}...')

        headers = {'User-Agent':
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
                   'Cache-Control': 'no-cache'}  # Disable caching in headers

        response = requests.get(site, proxies={'http': proxy, 'https': proxy}, headers=headers)

        if response.status_code == 200:
            # Construct the full path to the file within the folder
            full_path = os.path.join(folder_path, filename)

            # Downloaded content
            html_content = response.text

            if prettify:
                # Prettify the HTML content using BeautifulSoup (optional)
                soup = BeautifulSoup(html_content, 'html.parser')
                pretty_html = soup.prettify()
                html_content = pretty_html
            else:
                # Keep the content as-is
                pass

            with codecs.open(full_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f'{site} content written to {full_path}')
        else:
            print(f'Failed to download {site} (Status code: {response.status_code})')
    except requests.exceptions.RequestException as e:
        print(f'Error downloading {site}: {e}')


# Site List Scrapping
if __name__ == '__main__':
    sites_to_check = site_to_check

    # Call the function for each website (optionally with a proxy)
    for site in site_to_check:
        write_html_file(site)  # Without proxy
        # write_html_file(site, proxy='http://your_proxy_address:port')  # With proxy

# The Final Product

import subprocess
from datetime import date  # Import date for today's date
from bs4 import BeautifulSoup  # Import BeautifulSoup for parsing HTML
import csv  # Import csv library for writing
import os


def find_index_in_library(title, site_to_check):
    """
    This function checks if a title matches an entry in the site_to_check list and returns the corresponding index.

    Args:
        title: The title text to search for (usually from productTitle).
        site_to_check: The list of website URLs.

    Returns:
        The index of the matching entry in site_to_check, or -1 if not found.
    """
    for i, url in enumerate(site_to_check):
        # Extract the product name from the URL (assuming it's part of the path)
        url_parts = url.split('/')
        if len(url_parts) >= 4:  # Ensure there are at least 4 parts (3 slashes)
            product_name = url_parts[3].strip()  # Assuming product name is in the 4th position
        else:
            pass

        # Compare the title (lowercase) with the extracted product name (lowercase)
        if product_name and title.lower() == product_name.lower():
            return i  # Return the index if there's a match

        print(i, product_name)
        return -1
    # return -1  # Return -1 if not found


def check_price():
    # Run the proxy rotation (assuming proxy_rotation.py is a separate script)
    subprocess.run(["python", "proxy_rotation.py"])

    # Path to the folder containing HTML files
    folder_path = "downloaded_html"

    # Iterate over files in the folder
    for filename in os.listdir(folder_path):

        if filename.endswith(".html"):  # Check if it's an HTML file
            full_path = os.path.join(folder_path, filename)

            try:
                # Open the file and process its contents
                with open(full_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()

                    # Process the HTML content (extract price, etc.)
                    soup = BeautifulSoup(html_content, 'html.parser')

                    # Access and process the parsed HTML using BeautifulSoup methods
                    title = soup.find(id='productTitle').text.strip()
                    price = soup.find(class_='a-price-whole').text.strip() + soup.find(
                        class_='a-price-fraction').text.strip()
                    today = date.today()

                    index = find_index_in_library(title, site_to_check)
                    link = site_to_check[index]

                    print(f"Processing price data from {filename}")

                    # ----------------------------------Writing into a csv ------------------------------------
                    header = ['Title', 'Price', 'Date', 'Link']
                    data = [[title, price, today, link]]

                    # Check if the CSV file exists
                    file_exists = os.path.isfile('amazon_web_scrapper_dataset.csv')

                    if not file_exists:  # Create the CSV file if it doesn't exist
                        with open('amazon_web_scrapper_dataset.csv', 'w', newline='', encoding='utf-8') as f:
                            writer = csv.writer(f)
                            writer.writerow(header)
                            writer.writerows(data)
                        print('CSV file created successfully!')
                    else:  # Append data if the CSV file already exists
                        with open('amazon_web_scrapper_dataset.csv', 'a', newline='', encoding='utf-8') as f:
                            writer = csv.writer(f)
                            writer.writerows(data)
                        print('Data appended to existing CSV file.')

            except Exception as e:  # Catch any exceptions during processing or writing
                print(f"Error processing {filename}: {e}")

        print(title)
        print(filename)


if __name__ == "__main__":
    check_price()
