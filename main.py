from bs4 import BeautifulSoup
import mysql.connector
import time
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains




def Collection(page):
    # Using Beautiful soup to make contents iterable
    soup = BeautifulSoup(page, 'html.parser')
    val = []

    # Finding all instances of the class containing the players names
    rows = soup.find("tbody", class_="jsx-2006211681")
    # Iterating through data tables and placing them in tuples to be sent to SQL database
    for a in rows:
        temp_row = []
        for x in a:
            temp_row.append(x.text.strip())
        temp_row.pop(0)
        temp_row.pop(2)
        temp_row.pop(2)
        temp_row.pop(2)
        temp_row.pop(2)
        temp_row.pop(2)
        temp_row.pop(2)
        temp_row[1] = int(temp_row[1].replace(',',''))
        val.append(tuple(temp_row))
    print(val)
    return val








# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    mydb = mysql.connector.connect(
        host="localhost",
        user="noahalsina",
        database="mass_shootings"
    )

    mycursor = mydb.cursor()

    sql = "INSERT IGNORE INTO state_populations (state, 2022population) VALUES (%s, %s)"
    val = []
    driver = uc.Chrome()

    # url containing information being loaded into driver
    URL = 'https://worldpopulationreview.com/states'
    driver.get(URL)
    time.sleep(4)

    try:
        actions = ActionChains(driver)
        # Looping through all the pages until it reaches the last page

        for x in Collection(driver.page_source):
            val.append(x)
    except:
        pass
    finally:
        driver.quit

        # Executing the data to the SQL server
        print(val)
        mycursor.executemany(sql, val)
        mydb.commit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
