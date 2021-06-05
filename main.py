# Lets do this by tags and categories like action, strategy, etc... instead
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver


def store_category(link):
    browser = webdriver.Chrome()
    browser.get(link)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # ---
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")
    a = 0
    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        a = a + 1
        if a == 6:
            break

    soup = BeautifulSoup(browser.page_source, 'html.parser')

    new_category = []
    i = 0
    for div in soup.find_all("div", {"class": "search_results"}):
        for link in div.select("a"):
            new_category.append(link['href'])
            i = i + 1
            if i == 500:
                break

    return new_category


def get_store_data(store):
    response = requests.get(store)
    soup = BeautifulSoup(response.content, 'html.parser')

    # If a game page has all of the attribtues then we can collect its information
    if soup.find('span', attrs={'itemprop': 'name'}):
        if soup.find('span', attrs={'itemprop': 'description'}):
            # Gets the name of the game
            game_name = soup.find('span', attrs={'itemprop': 'name'}).next
            print(game_name)
            # Gets the score of the game

            # Gets the review category of the game
            game_review = soup.find('span', attrs={'itemprop': 'description'}).next
            print(game_review, end='\n')

            # Grabs the game review score
            if soup.find('span', attrs={'class': 'nonresponsive_hidden responsive_reviewdesc'}):
                div = soup.find_all("span", {'class': 'nonresponsive_hidden responsive_reviewdesc'})
                if len(div) == 2:
                    str1 = ""
                    for i in div[1]:
                        str1 += str(i)
                    str1 = str1.strip()
                    game_score2 = str1[2] + str1[3]
                    print(game_score2)
                else:
                    str1 = ""
                    for i in div[0]:
                        str1 += str(i)
                    str1 = str1.strip()
                    game_score2 = str1[2] + str1[3]
                    print(game_score2)

            #Grabs the price of the game including sales if applicable
            if(soup.find('div', attrs={'class':'discount_original_price'})):
                #Get the price
                all = soup.find('div', attrs={'class':'discount_original_price'}).next
                print("Original: " + all, end=" ")
                all = soup.find('div', attrs={'class': 'discount_final_price'}).next
                print("Discounted: " + all, end='\n\n')
            else:
                all = soup.find('meta', attrs={'itemprop':'price'})
                print("Original No sale: " + all["content"], end='\n\n')
            # Note Free games show up as 0.00

    # Things to collect information one.
    # Decide if we want to include DLC or Not
    # Achievement amounts (?)
    # content Rating (?)
    # Review Amount
    # Curator Review Amount
    # Game Feature Tags Ex, Controller Support

    # To find the price Work on Later
    # all = soup.find('meta', attrs={'itemprop':'price'})
    # all2 = all.get('content', '')
    # print(all2)
    # https://store.steampowered.com/app/1264280/Slipways/
    # https://store.steampowered.com/app/601840/Griftlands/
    # https://store.steampowered.com/app/1328670/Mass_Effect_Legendary_Edition/
    # "https://store.steampowered.com/app/211820/Starbound/"


# Sorts by Top Selling Action
New_List = store_category("https://store.steampowered.com/search/?tags=19&filter=topsellers")

for i in New_List[:-4]:
    get_store_data(i)

# Sorts by Top Sellers
# Top_List = store_category("https://store.steampowered.com/search/?filter=topsellers&os=win")

# Sorts by Upcoming
# Upcoming_List = store_category("https://store.steampowered.com/search/?filter=comingsoon&os=win")

# Sorts by Special
# Special_List = store_category("https://store.steampowered.com/search/?&specials=1")
