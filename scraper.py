import requests
from bs4 import BeautifulSoup
from os import system, name
import pickle
import os.path
import shutil

# ******************************************** #

# **********Prerequirements*************#
# 1.Beautifulsoup - pip install beautifulsoup4
# 2.Requests - pip install requests

# ********Future scopes**********#
# when the program is hosted on a web hosting server the program can be run from anywhere
# the products price list can be send through emails
# the program can be upgraded so that when a products price decreases beyond a limit a mail notification will be send to user
# auto ordering of specific products can be implemented by integrating the product with selenium(a python automation package)

# ******************************************** #

# gets terminal size
columns = shutil.get_terminal_size().columns

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}  # header for smooth browsing

# to clear the screen after each input


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


# product price details
def get_details(URL, choice):
    clear()
    page = requests.get(URL, headers=headers)  # get data from website
    soup = BeautifulSoup(page.content, 'html.parser')  # get page content

    if choice == "1":
        title = soup.find(id="productTitle").get_text().strip()
        # gets actual price of the product if it is given, mrp[0] will be empty if actual price is not shown
        mrp = soup.findAll("span", {"class": "priceBlockStrikePriceString a-text-strike"})
        if mrp != []:
             mrp = mrp[0].get_text().strip()
        else:
            # if the actual price is not given  we set mrp to this
            mrp = "Actual price not available"
        try:
            # deal price which is available in amazon
            deal = soup.find(id="priceblock_dealprice")
            # special amazon price NOTE: only deal price or amazon price will be given at a single time for a product
            amazonprice = soup.find(id="priceblock_ourprice")
            if deal:
                print(title, " ", mrp,
                      " ", deal.get_text().strip())
            elif amazonprice:
                print(title, " ", mrp,
                      " ", amazonprice.get_text().strip())
            else:
                print(title, " ", mrp[0])
        except:
            print("\nSORRY!!SOMETHING WENT WRONG PLZ TRY AGAINN....")
    elif choice == "2":
        title = soup.findAll("span", {"class": "B_NuCI"})
        mrp = soup.findAll(
            "div", {"class": "_30jeq3 _16Jk6d"})
        try:
            deal = soup.findAll(
                "div", {"class": "_3I9_wc _2p6lqe"})
            print(title[0].get_text().strip(), " ",
                  mrp[0].get_text().strip(), " ", deal[0].get_text().strip())
        except:
            print("\nSORRY!!SOMETHING WENT WRONG PLZ TRY AGAINN....")

# products list

def products_details(products):
    clear()
    if products.get("flipkart"):
        links = products["flipkart"]
        c = 1
        print("FLIPKART")
        for url in links:
            page = requests.get(url, headers=headers)  # get data from website
            # get page content
            soup = BeautifulSoup(page.content, 'html.parser')
            try:
                title = soup.findAll("span", {"class": "B_NuCI"})
                mrp = soup.findAll(
                    "div", {"class": "_30jeq3 _16Jk6d"})
                deal = soup.findAll(
                    "div", {"class": "_3I9_wc _2p6lqe"})
                print(c, ". ", title[0].get_text().strip(), " ",
                      mrp[0].get_text().strip(), " ", deal[0].get_text().strip())
            except:
                print("\nERROR WHILE FETCHING THE DETAILS..")
            c += 1
    if products.get("amazon"):
        links = products["amazon"]
        c = 1
        print("AMAZON")
        for url in links:
            page = requests.get(url, headers=headers)  # get data from website
            # get page content
            soup = BeautifulSoup(page.content, 'html.parser')
            title = soup.find(id="productTitle").get_text().strip()
            mrp = soup.findAll(
                "span", {"class": "priceBlockStrikePriceString a-text-strike"})
            if mrp != []:
                mrp = mrp[0].get_text().strip()
            else:
                mrp = "actual price not available"
            deal = soup.find(id="priceblock_dealprice")
            amazonprice = soup.find(id="priceblock_ourprice")
            # used mrp because findAll returns a list even if only one data is returned
            try:
                if deal:
                    print(c, ". ", title, " ", mrp,
                          " ", deal.get_text().strip())
                elif amazonprice:
                    print(c, ". ", title, " ", mrp,
                          " ", amazonprice.get_text().strip())
                else:
                    print(c, ". ", title, " ", mrp)
            except:
                print("\nSORRY!!SOMETHING WENT WRONG PLZ TRY AGAINN....")
            c += 1


def main():
    clear()
    # infinite while loop for menu
    # sendmail()
    print("\n\t\t\tWEB SCRAPING")
    print("\t\t\t*******************")
    while True:
        # get user choice for website
        choice = input("\nSelect the website from the following :\n\n\t1.Amazon\n\t2.Flipkart\n\t3.Add data to file\n\t4.Current products\n\t5.Quit \n\nEnter ur choice  : ".center(columns))
        clear()
        if choice == "1":
            print("**********")
            print("Amazon")
            print("**********")
            # get product url
            URL = input("Enter URL of the Product :")
            get_details(URL, choice)
        elif choice == "2":
            print("**********")
            print("Flipkart")
            print("**********")
            # get product url
            URL = input("Enter URL of the Product :")
            get_details(URL, choice)
        elif choice == "3":
            # check if file is present or not
            if os.path.isfile("products.pickle"):
                clear()
                try:
                    URL = input("Enter URL of the Product :")
                    pickle_in = open("products.pickle", "rb")
                    # gets current filedata
                    products = pickle.load(pickle_in)
                    pickle_in.close()
                    pickle_out = open("products.pickle", "wb")
                    # checking if url is from flipkart or amazon
                    if "flipkart" in URL.lower():
                        # works if product dictionary already have flipkart key
                        if products.get("flipkart"):
                            products["flipkart"].append(URL)
                        else:
                            products["flipkart"] = [URL]
                    elif "amazon" in URL.lower():
                        # works if product dictionary already have amazon key
                        if products.get("amazon"):
                            products["amazon"].append(URL)
                        else:
                            products["amazon"] = [URL]
                    # updates file with new products data
                    pickle.dump(products, pickle_out)
                    pickle_out.close()
                except:
                    pickle_in.close()
                    pickle_out.close()
            # if the file is not present
            else:
                clear()
                URL = input("Enter URL of the Product :")
                products = {}
                pickle_out = open("products.pickle", "wb")
                # checking if url is from flipkart or amazon
                if "flipkart" in URL.lower():
                    products["flipkart"] = [URL]
                elif "amazon" in URL.lower():
                    products["amazon"] = [URL]
                pickle.dump(products, pickle_out)
                pickle_out.close()
                print("New file created")
        elif choice == "4":
            try:
                pickle_in = open("products.pickle", "rb")
                products = pickle.load(pickle_in)
                products_details(products)
                pickle_in.close()
            except:
                print("\nSORRY!!NO PRODUCT AVAILABLE")
        elif choice == "5":
            clear()
            print("\nBYEE!!!")
            break
        else:
            clear()
            print("\nSORRY!!TRY AGAIN")


if __name__ == "__main__":
    main()
