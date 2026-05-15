import requests
from bs4 import BeautifulSoup
import smtplib
import os
import time

# --- ADD AS MANY PRODUCTS AS YOU WANT HERE ---
PRODUCTS = [
    {
        "name": "Induction Cooker Prestige 1600W",
        "url": "https://www.flipkart.com/prestige-1600-w-induction-cooktop-push-button/p/itmfd5167ac9e920?pid=ICTGHH6HQYJUZPA7&lid=LSTICTGHH6HQYJUZPA7BSYO68&marketplace=FLIPKART&q=induction&store=j9e%2Fm38%2F575&spotlightTagId=default_BestsellerId_j9e%2Fm38%2F575&srno=s_1_3&otracker=search&otracker1=search&fm=Search&iid=56befb22-b150-4b1f-af68-633e64105d1f.ICTGHH6HQYJUZPA7.SEARCH&ppt=sp&ppn=sp&ssid=nllyody8u80000001778863949617&qH=65f576a7ab0e9305&ov_redirect=true&ov_redirect=true",
        "target_price": 1500
    },
    {
        "name": "Induction Cooker Pigeon 1800W",
        "url": "https://www.flipkart.com/pigeon-1800-w-induction-cooktop-push-button/p/itm3893130ae5422?pid=ICTDZZM3SKDMH5CK&lid=LSTICTDZZM3SKDMH5CKBRUELK&marketplace=FLIPKART&q=induction&store=j9e%2Fm38%2F575&spotlightTagId=default_BestsellerId_j9e%2Fm38%2F575&srno=s_1_4&otracker=search&otracker1=search&fm=Search&iid=56befb22-b150-4b1f-af68-633e64105d1f.ICTDZZM3SKDMH5CK.SEARCH&ppt=sp&ppn=sp&ssid=nllyody8u80000001778863949617&qH=65f576a7ab0e9305&ov_redirect=true&ov_redirect=true",
        "target_price": 1300
    },
    {
        "name": "Zebronoics wireless Mouse",
        "url": "https://www.flipkart.com/zebronics-pulse-ambidextrous-optical-mouse-1200dpi-dual-bt-multi-connect-lightweight-comfort/p/itm95ea8032bd846?pid=ACCGXZ6CZBZKU6ZH&lid=LSTACCGXZ6CZBZKU6ZHHJQKLK&marketplace=FLIPKART&q=zebronics+wireless+mouse&store=6bo%2Ftia%2F8pp%2Fp0w&srno=s_1_3&otracker=search&otracker1=search&fm=Search&iid=227256c5-d7f4-436f-a054-355499d6d538.ACCGXZ6CZBZKU6ZH.SEARCH&ppt=sp&ppn=sp&ssid=hmhx4pmi4w0000001778864474795&qH=546e5465dc215dda&ov_redirect=true&ov_redirect=true",
        "target_price": 250
    }
    # {
    #     "name": "Second Item Name ",
    #     "url": "PASTE_SECOND_ITEM_URL_HERE",
    #     "target_price": 500
    # }
    # You can add more blocks like the ones above!
]

EMAIL_ADDRESS = os.environ.get("EMAIL_USER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASS")

def check_prices():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    for item in PRODUCTS:
        print(f"Checking price for: {item['name']}")
        try:
            response = requests.get(item['url'], headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")

            # Flipkart's price class
            price_element = soup.find("div", {"class": "Nx9bqj"})
            
            if price_element:
                current_price = int(price_element.get_text().replace('₹', '').replace(',', ''))
                print(f"Current Price: ₹{current_price}")

                if current_price <= item['target_price']:
                    print(f"Target hit for {item['name']}!")
                    send_mail(item['name'], current_price, item['url'])
                else:
                    print(f"Still above target (₹{item['target_price']}).")
            else:
                print(f"Could not find price for {item['name']}. UI might have changed.")
        except Exception as e:
            print(f"Error checking {item['name']}: {e}")

        # Added pause !
        print("Waiting 10 seconds before checking the next item...")
        time.sleep(10)

def send_mail(name, price, url):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # Create the root message and set headers
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"📊 Price Alert: {name} dropped to ₹{price}"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS

    # Create a structured HTML version of the message
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #28a745;">Price Drop Detected!</h2>
        <table style="border-collapse: collapse; width: 100%; max-width: 500px;">
          <tr style="background-color: #f2f2f2;">
            <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">Item</th>
            <td style="padding: 10px; border: 1px solid #ddd;">{name}</td>
          </tr>
          <tr>
            <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">Current Price</th>
            <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold; color: #d9534f;">₹{price}</td>
          </tr>
          <tr style="background-color: #f2f2f2;">
            <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">Action</th>
            <td style="padding: 10px; border: 1px solid #ddd;"><a href="{url}" style="color: #007bff; text-decoration: none;">View on Flipkart</a></td>
          </tr>
        </table>
        <p style="margin-top: 20px; font-size: 12px; color: #777;">Sent via your Flipkart Price Tracker Bot</p>
      </body>
    </html>
    """

    part2 = MIMEText(html, 'html')
    msg.attach(part2)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
    print(f"Structured email sent for {name}!")
    server.quit()

if __name__ == "__main__":
    check_prices()