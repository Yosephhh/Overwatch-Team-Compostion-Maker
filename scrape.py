#****************************************************************************************************
#* Author: Yoseph Mamo
#* Filename: scrape.py
#* Purpose: Scrape players information (Live, Real Time In-Game Statistics) from  Overbuff.coma and parse results 
#* 
#****************************************************************************************************

import re
from bs4 import BeautifulSoup
from requests import get
from fake_useragent import UserAgent
import itertools


def get_player_data(player, battleTag, responce):
    """ 

    Function to scrape players information (Live, Real Time In-Game Stats) from his/her overbuff account and 
        parse the result to get the quickscore, heroes played and their wins, overall number of wins, profile icon link .. etc 
        Updates the caling object with the new informartion that was scraped
    
    Parameters: 
        (int):         battle_tag :  The battle tag of the player
        (string):      player_name:  The name of the player        
    
    Returns: 
        None

    """
    # Convert responce to a "soup" object by passing it to the soup constructor, and specify lxml as encoder 
    soup = BeautifulSoup(responce.text, 'lxml')
    # List to store Hero Names and Quick Scores 
    heroes = []
    # Loop Through each HTML tag under '<div>' : class: 'name' and look for name contents
    # In children, decode and output contents 
    for parent in soup.find_all('div', {'class': 'name' }): # Specify the parent classes name, type(bs4.element.Tag)
        for child in parent.findChildren('a', recursive = False):  # Access all of its children, store inside child var type(bs4.element.Tag)    
            heroes.append(child.decode_contents())                 # Get the contents of the child, add to the heroes list type(str)
    
    quick_scores   = [] # To Store the quickscores 
    # Loop Through each HTML tag under 'div' : class: group special and look for name 
    #contents In children, decode and output contents, 
    for parent in soup.find_all('div', {'class': 'group special' }):
            children = parent.findChildren('div', recursive = False)
            if not 'padded' in children[1].get('class'):
                quick_scores.append(children[1].findChildren('div', {'class': 'value' }, recursive = False)[0].decode_contents())
     
    player_image_link ="" 

    # Get the profile Icon of the player
    for link in soup.find_all('div', {'class': 'image-with-corner' }):
        images = link.find_all('img')
        for img in images:
            if "image-player" in img['class']:   
                player_image_link = img['src']

    # Get the number of wins from each hero and overall number of wins by the player
    # This time using regex, because why not :>
    temp = re.findall("<span class=\"color-stat-win\">[0-9]+</span>", responce.text)
    i = 0
    hero_wins = []
    for elt in temp: 
        if i < len(quick_scores)+1:
            val = re.sub("[^0-9]", "", elt)
            hero_wins.append(val)
            i = i+1
            
    player.total_wins = hero_wins[0] # First item is Overall wins by player so far
    hero_wins.pop(0)       
    player.hero_wins = hero_wins # other elements are wins from heroes
    
    # Convert scores to numeric format i.e 11,534 to 11534
    numeric_scores = []
    for x in quick_scores:
        numeric_scores.append(int(x.replace(',', '')))
    
    player.battle_tag = battleTag
    player.heroes = heroes
    player.quick_scores = numeric_scores
    player.player_logo = player_image_link


def get_responce(player_name, battle_tag):
    """ 

    Function make a request to overbuff.com with the specified BattleTag
    
    Parameters: 
        (int):         battle_tag :  The battle tag of the player
        (string):      player_name:  The name of the player        
    
    Returns: 
        (responce object) : responce : the responce from overbuff
        (string)          : url      : the url of the player

    """
    # Generate a fake User Agent
    ua = UserAgent()
    # Specify the URL, store inside string variable    
    url = 'https://www.overbuff.com/players/pc/' + player_name + '-' + battle_tag 
    # Call requests.get() to get responce object.

    responce = get(url, headers={'User-Agent': ua.chrome})

    # Uncomment to see live attempts for making requests to overbuff
    # if responce.status_code == 200:
    #     print(url, "  Responce Code: ", responce.status_code)
    # else:
    #     print(url, "  Responce Code: ", responce.status_code)

    return responce, url

def match_test_cases(player_name, battle_tag, cmdLargs = False):
    """ 

    Function check other cases of the battletag if entered case in-sensitive 
    
    Parameters: 
        (int):         battle_tag :  The battle tag of the player
        (string):      player_name:  The name of the player 
        (bool):     cmdLargs   :  True / False if command line arguments are in use       
    
    Returns: 
        (responce object) : responce : the responce from overbuff
        (string)          : url      : the url of the player

    """
    responce, url = get_responce(player_name, battle_tag)

    # Here I am Using Recurson to try to match several test Cases for user Friendlieness
    if cmdLargs:
        if responce.status_code != 200:
            print("\nError ! Invalid Battle Tag! Please Fix => ({})".format(player_name+'#'+battle_tag))
            # exit()
            responce , url = match_common_combinations(player_name, battle_tag)
            if responce.status_code != 200:
                responce , url = match_all_possible_combinations(player_name, battle_tag)
                if responce.status_code != 200:
                    print("\nError ! BattleTag Does Not Exist! Please Fix => ({})".format(player_name+'#'+battle_tag))
                    exit()
            else:
                return responce, url

        return responce, url
    else:
        if responce.status_code != 200:
            responce , url = match_common_combinations(player_name, battle_tag)
            if responce.status_code != 200:
                responce , url = match_all_possible_combinations(player_name, battle_tag)
            else:
                return responce, url

    #else return the default responce
    print("Done Checking !")
    return responce, url

def match_common_combinations(player_name, battle_tag):
    """ 

    Function check for the most common BattleTag cases intems of upper and lower case combinations
        Example: If the correct Tag was Rhino#12345 and the user entered rhino#123
        This function will check convert the name to titlecase (rhino to Rhino)
        and will make another request to overbuff, Instead of terminating the program.
    
    Parameters: 
        (int):         battle_tag :  The battle tag of the player
        (string):      player_name:  The name of the player 
    
    
    Returns: 
        (responce object) : responce : the responce from overbuff
        (string)          : url      : the url of the player

    """
    responce, url = "", ""
   # #Case 1: the default for overbuff.com titlecase playername-battletag
    # print(" 1. Trying Title Case: ", end = " ")
    responce, url = get_responce(player_name.title(), battle_tag)
    if responce.status_code == 200:
        return responce, url
    else:
        # print(" 2. Trying Lower Case: ", end = " ")
        responce, url = get_responce(player_name.lower(), battle_tag)
        if responce.status_code == 200:
            return responce, url
        else:
            # #Case 3: some players with uppercase playername-battletag
            # print(" 3. Trying Upper Case: ", end = " ")
            responce, url = get_responce(player_name.upper(), battle_tag)
            if responce.status_code == 200:
                return responce, url
            else:
                return responce, url

    return responce, url


def match_all_possible_combinations(player_name, battle_tag):
    """ 

    Function check for all the possible BattleTag cases intems of upper and lower case combinations.
        Frist creates a list of all the possible combinations of the playerName and continously 
        make a new request to overbuff, until the responce code is 200.

        Example: If the correct Tag was Rhino#12345 and the user entered 
        any of combinations such as (rHino#123, RHino#123, RhInO#123 ...)
       
       This function will match the correct tag (After several attempts ofcourse)
       
    Parameters: 
        (int):         battle_tag :  The battle tag of the player
        (string):      player_name:  The name of the player 
    
    
    Returns: 
        (responce object) : responce : the responce from overbuff
        (string)          : url      : the url of the player

    """
    # Ref: https://stackoverflow.com/questions/11144389/find-all-upper-lower-and-mixed-case-combinations-of-a-string
    all_combinations = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in player_name)))
    responce, url = "", ""
    for name in all_combinations:
        # print("Trying Case {} ".format(name), end = "  ")
        responce, url = get_responce(name, battle_tag)
        if responce.status_code == 200:
            return responce, url
    
    return responce, url



