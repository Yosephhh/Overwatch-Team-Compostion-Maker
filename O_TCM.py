# !/usr/bin/env python3.5
#****************************************************************************************************
#* Author: Yoseph Mamo
#* Filename: O_TCM.py
#* Purpose: SCrapes players information from overbuff.com and uses the hungarian algorithm to 
#*          obtain the best optimum team for an overwatch game.
#* 
#****************************************************************************************************
import sys
import re
import os
import json
import hungarian as h
import scrape
from pprint import pprint
from prettytable import PrettyTable
import time


MIN_PLAYERS = 2
MAX_PLAYERS = 7

# Class to represent players and their information
class player:    
    # All the Available Heroes in overwatch
    overwatch_heroes  = ['Ana', 'Ashe', 'Ball', 'Baptiste', 'Bastion', 
                            'Brigitte', 'D.Va', 'Doomfist', 'Genji', 
                            'Hanzo', 'Junkrat', 'Lúcio', 'McCree', 'Mei', 'Mercy', 
                            'Moira', 'Orisa', 'Pharah', 'Sigma','Reaper', 'Reinhardt', 
                            'Roadhog', 'Soldier: 76', 'Sombra', 'Symmetra', 
                            'Torbjörn', 'Tracer', 'Widowmaker', 'Winston', 
                            'Zarya', 'Zenyatta']
    # Their corresponding classes 
    ow_heroes_class  = ['Support', 'Damage', 'Tank', 'Support', 'Damage', 
                        'Support', 'Tank', 'Damage', 'Damage', 
                        'Damage', 'Damage', 'Support', 'Damage', 'Damage', 'Mercy', 
                        'Moira', 'Tank', 'Damage', 'Tank','Damage', 'Tank', 
                        'Tank', 'Damage', 'Damage', 'Damage', 
                        'Damage', 'Damage', 'Damage', 'Tank', 
                        'Tank', 'Support']
    player_name  = ""
    total_wins   = 0
    quick_scores = []
    heroes       = []    # The heroes that the player played with
    hero_wins    = []
    player_logo  = ""
    battle_tag   = ""
    # Create a copy of all the heroes
    complete_heroes = []
    # create an array to hold all the OW heroes along with their quick scores (0 if the player hasn't played them yet)!
    complete_scores = []
    # Array to hold the complete list of heroes and their wins
    complete_hero_wins = []
    
    def fill_zeroes(self):      
        """ 
        Function to fill in zeroes as the quick scores for the heroes that the players didn't play with  
  
        Parameters: 
            self: The player object / Instance 
          
        Returns: 
            None
        """
        #intersection = list(set(self.complete_heroes) & set(self.heroes))
        difference = list(set(self.overwatch_heroes) - set(self.heroes))
        self.complete_heroes = self.heroes.copy()#.extend(difference)

        for i in range(len(difference)):
            self.complete_heroes.append(difference[i])
        self.complete_scores = self.quick_scores.copy()#[0 for x in range(len(heroes))]
        # Fill the zeros as quickScores for the remaining heroes
        for i in range(len(difference)):
            self.complete_scores.append(0)
        # Keep this line ! sometimes Adds Extra 0 for soldier: 76 as just 76
        # for older versions of overbuff.com
        if len(self.complete_scores) > len(self.overwatch_heroes):
            self.complete_heroes.pop()
        # Now Sort the List
        heros_and_quick_scores = zip(self.complete_heroes, self.complete_scores)       
        heros_and_quick_scores = sorted(heros_and_quick_scores)

        temp_heroes = []
        temp_scores = []
        temp_hero_wins = []

        for item in heros_and_quick_scores:
            temp_heroes.append(item[0])
            temp_scores.append(item[1])
    
        self.complete_hero_wins = [x*0 for x in range(32)]
        
        for i  in range(0, len(self.complete_heroes)):
            hero_index = self.heroes.index(self.complete_heroes[i]) if self.complete_heroes[i] in self.heroes else -1
            if hero_index != -1:
                temp_hero_wins.append(self.hero_wins[hero_index])
            else:
                temp_hero_wins.append('0')
        
        self.complete_heroes = temp_heroes
        self.complete_scores = temp_scores
        self.complete_hero_wins = temp_hero_wins
        # At this point we have All OW heroes and their quick scores generated            

    
    def sort_heroes(self):
        """ 

        Function to sort the heroes alphabetically in asc order after scrape
  
        Parameters: 
            self: The player object / Instance 
          
        Returns: 
            None
        """
        # Zip the heroes list and QuickScores list
        heros_and_quick_scores = zip(self.heroes, self.quick_scores)
        # Sort them according to hero names alphabetically 
        heros_and_quick_scores = sorted(heros_and_quick_scores)
        self.heroes = []
        self.quick_scores = []
        for item in heros_and_quick_scores:
            self.heroes.append(item[0])
            self.quick_scores.append(item[1])

        return heros_and_quick_scores
            
    def display_player_info(self):
        """ 

        Function to Display players Info Initially after scrape without changes made 
  
        Parameters: 
            self: The player object / Instance 
          
        Returns: 
            None
        """
        print("Player Name: ", self.player_name)
        print("{:14s}    {:6s}   {:} \n".format("Heroes", "Quick Scores", "wins with This Hero"))
        for i in range(0,len(self.heroes)):
            print("{}: {:14}    {:6}   {:6} ".format(i+1, self.heroes[i], self.quick_scores[i], self.hero_wins[i]))
        print('\n\n')

    def display_final_player_info(self):
        """ 

        Function to Display players Info Initially after scrape after changes made 
        changes may include:
                A) sorting the heroes and scores.
                B) Getting '0' for heroes that weren't used before 
        Parameters: 
            self: The player object / Instance 
          
        Returns: 
            None
        """
        print("Player Name: ", self.player_name)
        print("{:14s}    {:6s}  {} \n".format("Heroes", "Quick Scores", "wins with This Hero"))
        for i in range(0,len(self.complete_heroes)):
            print("{}: {:14}    {:6}    {:6} ".format(i+1, 
                  self.complete_heroes[i], self.complete_scores[i],
                  self.complete_hero_wins[i]))
        print('\n\n')

def getNumPlayers():
    """ 

    Function to get the number of players playing from the user

    Parameters: 
        None
        
    Returns: 
        (int): num_players:  The number of players
    """

    print("\nWelcme To Overwatch Team Composition Maker.\n")
    print("A Coaching Tool For The Modern Era!\n")


    num_players = input("Enter the Number of Overwatch Players in Your Team. ( Must Be Between {} and {} ): ".format(MIN_PLAYERS, MAX_PLAYERS))
    if num_players.isdigit() != True:
        print("\nError ! Invalid Input (Input Must Be Numeric) !!")
    else:
        if int(num_players) > MAX_PLAYERS or int(num_players) < MIN_PLAYERS:
            print("\nError !  Invalid Input (Invalid Rage Must Be Between {} and {} ): ".format(MIN_PLAYERS, MAX_PLAYERS))
            exit()
        else:
            return int(num_players)    
    exit()

def get_player_info(valid):
    """ 

    Function to Prompt the user fot the players information (BattleTag)
    
    Parameters: 
        valid: counter variable used as static variable to keep track of players 
        
    Returns: 
        (int):    player_name:  The name of the player
        (string): battle_tag :  The battle tag of the player
    """
    user_name = ""
    if valid is True:
        get_player_info.player_count += 1
        
    if(get_player_info.player_count == 1):
        print("Usage: Enter Player ID Like (playerName#battleTag) EX. Rhino#1234 \n") 
    
    user_id = input("Enter Player {}'s ID: ".format(get_player_info.player_count))    
    
    #check if a userId has a '#' symbol to begin with ie. playername#battletag
    while '#' not in user_id: 
        print("\nUsage: \nPlease Enter a Valid User Id !!")
        print("Enter Player ID Like (playerName#battleTag) EX. Rhino#1234 \n") 
        user_id = input("Enter Player {}'s ID: ".format(get_player_info.player_count))

    user_name = user_id.split("#")   
    player_name, battle_tag = user_name[0], user_name[1]

    return player_name , battle_tag


def check_player_info(player_name, battle_tag, cmdLargs = False):
    """ 

    Function to Check if the user Entered a valid player name and battle tag
    
    Parameters: 
        (int):      player_name:  The name of the player
        (string):   battle_tag :  The battle tag of the player
        (bool):     cmdLargs   :  True / False if command line arguments are in use
        
    Returns: 
        (list)  player_info:  a list containgin player_name, battle_tag, and  responce
        reponce is a return form the get function from the requests module

    """
    responce , url  = scrape.match_test_cases(player_name, battle_tag, cmdLargs)
    #print("URL: ", url) # Display the URL 
    #Check if the request for the website succeeded , 200 =  success, 404 responce code  = no webpage found 
    if responce.status_code != 200 :
        print("\nError ! Invalid Battle Tag! Please Fix => ({})".format(player_name+'#'+battle_tag))
        # print("Invalid overbuff.com URL : ", url) # Display the URL 
        # print("Overbuff.com responce code: ", responce.status_code)
        # print("Please Try Again. !!!!!!!!!!!!!!!\n")
        player_name , battle_tag = "", ""
        player_name , battle_tag = get_player_info(False) 
        check_player_info(player_name, battle_tag);

    player_info = [player_name, battle_tag, responce]

    return player_info
    

def generateMatrix(players, cmdLargs = False):
    """ 

    Function to Generate Matrix from the players scraped infromation 

    
    Parameters: 
        (list): players    : an array of player objects
        (bool): cmdLargs   :  True / False if command line arguments are in use
        
    Returns: 
        (nxm list)  quick_scores_matrix:  a matrix containing the quick scores of 
                                          the players.
        
    """
   
    players_list,battle_tags_list = [], []
    num_players = len(players)
    if cmdLargs:
        sys.argv.pop(0)
        battle_tags = sys.argv
        str1 = ' '.join(map(str, battle_tags)) 
        battle_tags = str1.split(' ')
        players_list = []
        battle_tags_list =[]
        for i in range(num_players):
            vals = battle_tags[i].split('#')
            players_list.append(vals[0])
            battle_tags_list.append(vals[1])

        for i in range(num_players):
            player_name, battle_tag = players_list[i], battle_tags_list[i]   
            player_info = check_player_info(player_name, battle_tag, True)
            players[i].player_name = player_info[0]      
            scrape.get_player_data(players[i], battle_tag, player_info[2])
            # Fill Zeros as quickscores for the heroes the player hasn't played with.
            players[i].fill_zeroes()
    else:
        for i in range(num_players):   
            player_name, battle_tag = get_player_info(True)
            player_info = check_player_info(player_name, battle_tag)
            players[i].player_name = player_info[0]      
            scrape.get_player_data(players[i], battle_tag, player_info[2])
            # Fill Zeros as quickscores for the heroes the player hasn't played with.
            players[i].fill_zeroes()

    # Make up the Hungarian Matrix
    quick_scores_matrix = []
    for i in range(num_players):
        quick_scores_matrix.append(players[i].complete_scores)
    
    
    # Hungarian tries to minimize the cost matrix, 
    # since maximizing profit is the same as minimizing cost
    # reverse the costs: x -> -x. this makes '0' becomes the largest number possible.
    # Multiply the cost matrix by -1 for maximization.
    for i in quick_scores_matrix:
        for j in range(len(i)):
            i[j] = -1*i[j]
    
    # pprint(quick_scores_matrix)
    return quick_scores_matrix


def applyHungarian(quick_scores_matrix):
    """ 

    Function to use the hangarian matrix after the quick scores matrix is ready
    
    Parameters: 
       (nxm list)  quick_scores_matrix:  a matrix containing the quick scores of 
                                          the players.
        
    Returns: 
       (tuple): result_index the index of the the optimal results in the matrix
       (tuple): heroes_index the location of the optimal hero in the matrix
       (tuple): scores_index the location of the optimal score in the matrix

    """
    
    # Now the Hungarian part
    hungarian = h.Hungarian(quick_scores_matrix, is_profit_matrix=False)
    hungarian.calculate()
    result_index = hungarian.get_results()
    
    result_index.sort()
    heroes_index = []
    scores_index = []
    
    for item in result_index:
        heroes_index.append(item[0])
        scores_index.append(item[1])
               
    return result_index, heroes_index, scores_index
  
def displayFinalOptimumTeam(result_index, heroes_index, scores_index ):
    """ 

    Function Display the final results on a Table Using PrettyTable 

    Parameters:
       (tuple): result_index the index of the the optimal results in the matrix
       (tuple): heroes_index the location of the optimal hero in the matrix
       (tuple): scores_index the location of the optimal score in the matrix
       
    Returns:
        None

    """
    table = PrettyTable()
    table.title="Final Optimum Team"
    table.field_names = ['Player\'s Name','Total Wins', 'Hero', 'HeroClass',
    'wins with This Hero','Quick Scores'] 
    #table.align["Hero"] = "l" # Left align player names
    table.padding_width = 1 # spacing between columns and edges (default)
    for i in range(len(result_index)):
        table.title = 'Final Optimum Team' # setting title for pTable
        player = players[i].complete_heroes[scores_index[i]]
        player_index = players[i].heroes.index( str(player))
        table.add_row([players[i].player_name, 
                       players[i].total_wins,
                       players[i].complete_heroes[scores_index[i]],
                       players[i].ow_heroes_class[scores_index[i]],
                       players[i].hero_wins[player_index],
                       players[i].quick_scores[heroes_index[i]]                                           
                       ])
    # print("\n",table.get_string(title="Final Optimum Team")) # setting title for pTable
    # print(table.get_string().split('\n', 1)[0])
    print(str(table))

def outputFinalOptimumTeamViaCsv(result_index, heroes_index, scores_index ):
    """ 

    Function Display the final results via CSV Fromat, also save this content to a file 
        Usefull Fro AJAX calls and any GUI related tasks. 
        Output contains as links to players bio, and profile and hero icons

    Parameters:
       (tuple): result_index the index of the the optimal results in the matrix
       (tuple): heroes_index the location of the optimal hero in the matrix
       (tuple): scores_index the location of the optimal score in the matrix
       
    Returns:
        None
        
    """
   
    str1 = 'Player\'s Name,Total Wins,Hero,HeroClass,wins with This Hero,QuickScores\n'
    for i in range(len(result_index)):
        player = players[i].complete_heroes[scores_index[i]]
        player_index = players[i].heroes.index( str(player) )
        str1 +=("{},{},{},{},{},{}\n".format(players[i].player_name, 
                       players[i].total_wins,
                       players[i].complete_heroes[scores_index[i]],
                       players[i].ow_heroes_class[heroes_index[i]],
                       players[i].hero_wins[player_index],
                        players[i].quick_scores[heroes_index[i]]
                       ))
    print((str1));

def outputFinalOptimumTeamViaJson(result_index, heroes_index, scores_index ):
    """ 

    Function Display the final results via Json Fromat, also save this content to a file 
        Usefull Fro ajax calls adn any GUI related tasks as it has linkes to players bio
        and profile and hero icons

    Parameters:
       (tuple): result_index the index of the the optimal results in the matrix
       (tuple): heroes_index the location of the optimal hero in the matrix
       (tuple): scores_index the location of the optimal score in the matrix
       
    Returns:
        None
        
    """
    str1 = 'Player\'s Name,Total Wins,Hero,wins with This Hero,QuickScores\n'
    d = {}
    for i in range(len(result_index)):
        playerName = str(players[i].player_name)
        d[playerName] = {}   
    for i in range(len(result_index)):
        player = players[i].complete_heroes[scores_index[i]]
        player_index = players[i].heroes.index( str(player) )
        d[players[i].player_name]['BattleTag'] = players[i].battle_tag
        d[players[i].player_name]['TotalWins'] = players[i].total_wins
        d[players[i].player_name]['Hero'] = players[i].complete_heroes[scores_index[i]]
        d[players[i].player_name]['HeroClass'] = players[i].ow_heroes_class[heroes_index[i]]
        d[players[i].player_name]['WinsWithThisHero'] = players[i].hero_wins[player_index]
        d[players[i].player_name]['QuickScore'] = players[i].quick_scores[heroes_index[i]]
        d[players[i].player_name]['logo'] = players[i].player_logo
    
    # outputJson = json.dumps(d)
    outputJson = json.loads(json.dumps(d))
    outputJson = json.dumps(outputJson, indent=2)
    print("\n\nFinal Optiaml Team Information In JSON \n")
    print((outputJson));

    # Write to The File
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_name = dir_path+'\\team.json.txt' 
    with open(file_name, "w+") as outputFile:
        outputFile.write(outputJson)
     # json.dump((d), outputFile)
 

if __name__ == "__main__":
    get_player_info.player_count = 0
    # Handle cmd line arguments
    if len(sys.argv) > 2:
        if len(sys.argv) <= MAX_PLAYERS and len(sys.argv) >= MIN_PLAYERS:
            # Create a list of player objects
            players = [player() for i in range(len(sys.argv) -1)]
            quick_scores_matrix = generateMatrix(players, True)
        else:
            print("\nError !  BattleTags Must Be Between {} and {} : ".format(MIN_PLAYERS, MAX_PLAYERS))
            exit()
    else:
        num_players = getNumPlayers()
        print("Num_players = ", num_players)
        # Create a list of player objects
        players = [player() for i in range(num_players)]
        # Generate the Matrix with Quick scores read From Players
        quick_scores_matrix = generateMatrix(players, False)

    #Get the resulting optimum Team
    result_index, heroes_index, scores_index = applyHungarian(quick_scores_matrix)
    #Display the final Optimum Team.
    displayFinalOptimumTeam(result_index, heroes_index, scores_index)
    outputFinalOptimumTeamViaJson(result_index, heroes_index, scores_index)
