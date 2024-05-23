# import requests
# import codecs
#
#
# with open('valid_proxy_list', 'r') as f:
#     proxies = f.read().split('\n')
#
# site_to_check = ['https://www.amazon.com/Funny-Data-Systems-Business-Analyst/dp/B07FNW9FGJ',
#                  'https://www.amazon.com/SanDisk-Endurance-microSDXC-Adapter-Monitoring/dp/B07P4HBRMV/?_encoding=UTF8&ref_=pd_hp_d_atf_ci_mcx_mr_hp_atf_m' ]
#
# counter = 0
#
# for site in site_to_check:
#     while True:  # Loop for proxy retries
#         try:
#             proxy = proxies[counter]
#             print(f'Using the proxy: {proxy}')
#             res = requests.get(site, proxies={'http': proxy, 'https': proxy})
#
#             if res.status_code == 200:
#                 with codecs.open('amazon_product_page.html', 'w', encoding='utf-8') as f:
#                     f.write(res.text)  # Write the raw HTML content
#                 print(f'{site} content written to amazon_product_page.html')
#                 break
#             else:
#                 print(f'Failed with status code: {res.status_code}')  # Handle other status codes
#         except requests.exceptions.RequestException as e:
#             print(f'Failed with exception: {e}')
#
#         # Move to the next proxy, ensuring a circular rotation
#         counter += 1
#         counter %= len(proxies)
#
#
##============================================================================================================== V1

import requests
import codecs
from urllib.parse import urlparse  # For filename extraction
import os  # For folder creation

from bs4 import BeautifulSoup


def write_html_file(site, proxy=None, folder_path='downloaded_html', prettify=False):
    """
    Attempts to download the content of a website using a proxy and writes it to a file
    within a specified folder. Optionally, prettifies the downloaded HTML content.

    Args:
        site (str): The URL of the website to access.
        proxy (str, optional): The proxy address (e.g., 'http://127.0.0.1:8080'). Defaults to None.
        folder_path (str, optional): The path to the folder where HTML files will be saved. Defaults to 'downloaded_html'.
        prettify (bool, optional): Whether to prettify the downloaded HTML content before writing (improves readability). Defaults to False.
    """

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
    return site

# Site List of What you want to scrape
if __name__ == '__main__':
    site_to_check = [
                    #Fresh Produce
                    'https://www.amazon.com/Organic-Honeycrisp-Apple-One-Medium/dp/B001GIP2A8/ref=sr_1_3_f3_wg?almBrandId=QW1hem9uIEZyZXNo&fpw=alm&s=amazonfresh&sr=1-3',
                    'https://www.amazon.com/Dole-Organic-Bananas-Bag/dp/B07ZLF9G83?pd_rd_i=B07ZLF9G83&fpw=alm&almBrandId=QW1hem9uIEZyZXNo&ref_=pd_alm_fs_dsk_sf_ai_16318981_1_1_i',
                    'https://www.amazon.com/produce-aisle-Strawberries-1-lb/dp/B000P6J0SM?pd_rd_i=B000P6J0SM&fpw=alm&almBrandId=QW1hem9uIEZyZXNo&ref_=pd_alm_fs_dsk_sf_ai_16318981_1_3_i',
                    'https://www.amazon.com/Shrimp-White-Farm-Raised-Frozen/dp/B07FZFB494?pd_rd_i=B07FZFB494&fpw=alm&almBrandId=VUZHIFdob2xlIEZvb2Rz&ref_=pd_alm_wf_dsk_dp_dzrp_1_6_i',
                    'https://www.amazon.com/Seafood-Halibut-Fillet-Msc/dp/B07HMC7VGJ?pd_rd_i=B07HMC7VGJ&fpw=alm&almBrandId=VUZHIFdob2xlIEZvb2Rz&ref_=pd_alm_wf_dsk_dp_dzrp_1_2_i'
                     ]

    # Call the function for each website (optionally with a proxy)
    for site in site_to_check:
        write_html_file(site)  # Without proxy
        # write_html_file(site, proxy='http://your_proxy_address:port')  # With proxy


##=============================================================================================================== V2




