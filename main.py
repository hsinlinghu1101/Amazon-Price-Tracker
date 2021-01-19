from bs4 import BeautifulSoup
import requests
import smtplib
import config
import lxml

my_email = config.my_email
my_password = config.my_password
target_product_url = [
    "https://www.amazon.com/All-new-Kindle-Oasis-adjustable-auto-renewal/dp/B07VCMKB84/ref=zg_bs_electronics_92?_encoding=UTF8&refRID=FFPFV3M5J2N77SWMGC4T&th=1",
    "https://www.amazon.com/Embryolisse-Concentre-Concentrated-Miracle-2-54-oz/dp/B007PM1A82/ref=pd_nav_hcs_rp_1?pd_rd_w=2t9OX&pf_rd_p=0381b3ca-ac9b-49b9-ba63-35fd0815ad67&pf_rd_r=QH0X1DGNB6W1VR81D5VG&pd_rd_r=e2fcfef9-a03e-4f34-9370-4e8100b25e6f&pd_rd_wg=TKZ60&pd_rd_i=B007PM1A82&psc=1",
    "https://www.amazon.com/Samsonite-56844-Luggage-Carry-On-Charcoal/dp/B00EALLN42/ref=sr_1_4?crid=S289FWSK9ZE5&dchild=1&keywords=samsonite+luggage&qid=1610488620&sprefix=samso%2Caps%2C217&sr=8-4"
]
lowest_price = [199.99, 13.15, 61.99]

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
    "Accept-Language":"en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7"
}
message = []
for i in range(len(target_product_url)):
    amz_response = requests.get(url=target_product_url[i], headers=headers)
    html_doc = amz_response.text

    soup = BeautifulSoup(html_doc, "lxml")
    price_code = soup.find(name="span", class_="a-size-medium a-color-price priceBlockBuyingPriceString")
    price = "".join(list(price_code.get_text())[1:])
    target_product_code = soup.find(name="span", class_="a-size-large product-title-word-break")
    target_product = target_product_code.get_text().strip()
    if float(price) <= lowest_price[i]:
      message.append(f"{target_product}\nNow ${price}\nCheck on Amazon! {target_product_url[i]}\n")

message = '\n'.join(message)

with smtplib.SMTP("smtp.gmail.com", 587) as connection:
    connection.starttls()
    connection.login(user=my_email, password=my_password)
    connection.sendmail(from_addr=my_email, to_addrs=my_email,
                        msg=f"subject:Amazon Deals!\n\nHey! Don't miss the deals!\n{message}".encode('utf-8'))

