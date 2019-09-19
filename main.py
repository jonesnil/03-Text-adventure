import sys, logging, json

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Game loop functions
def render(game,current,moves,points,areaInfo):    
    ''' Displays the current room, moves, and points '''    
    r = game['rooms']    
    c = r[current]
    
    
    if areaInfo == True:
        print('\n\n')
        print(c['desc'])

    printExits(game, current)
    if len(c['inventory']):        
        print('You see the following items:')        
        for i in c['inventory']:           
            print('\t{i}'.format(i=i))

def getInput(game,current,verbs):    
    ''' Asks the user for input and normalizes the inputted value. Returns a list of commands '''    
    toReturn = input('\nINPUT: ').strip().upper().split()    
    if (len(toReturn)):        
        #assume the first word is the verb        
        toReturn[0] = normalizeVerb(toReturn[0],verbs)    
        return toReturn

def update(selection,game,current,inventory):    
    if selection is None:        
        print("\nWe don't have time for this.")        
        return 'JUSTTEXT'
    ''' Process the input and update the state of the world '''    
    s = list(selection)[0]  
    #We assume the verb is the first thing typed    
    if s == "":        
        print("\nInput not recognized.")        
        return 'JUSTTEXT'
    elif s == 'EXITS':        
        printExits(game,current)        
        return current    
    else:        
        for e in game['rooms'][current]['exits']:
            if s == e['verb'] and e['target'] == 'JUSTTEXT':
                print('\n\n')
                print(e['condition'])
                return ['JUSTTEXT', True]
            elif s == e['verb'] and  s == 'BUILD':
                if(len(inventory) >= 5):
                    print('\n\n')
                    print(e['condition'])
                    sys.exit()
                if 'Fountain Valve' in inventory:
                    print('\n\n')
                    print('Why are you staring at the fountain like that? Do you have something in mind? You already flooded it.\nIt\'s completely overflowing now.')
                    return ['JUSTTEXT', True]
                print('\n\n')
                print('Why are you staring at the fountain like that? Do you have something in mind?')
                return ['JUSTTEXT', True]
            elif s == e['verb'] and  s == 'TAKE':
                if e['target'] in inventory:
                    print('\n\nWhat are you looking at? You already took that.')
                    return ['JUSTTEXT', True]
                print('\n\n')
                print(e['condition'])
                print('\n You got the ' + e['target'] + '!')
                inventory.append(e['target'])
                return ['JUSTTEXT', True]
            elif s == e['verb'] and e['condition'] != '':
                print('\n\n')
                print(e['condition'])
                return [e['target'], False]
            elif s == e['verb'] and e['target'] != 'NoExit':                
                return [e['target'], True]    
            
    print("\nYou can't go that way!")    
    return current

def printExits(game,current):    
    e = ", ".join(str(x['verb']) for x in game['rooms'][current]['exits'])    
    print('\nYour options include: {directions}'.format(directions = e))
        
def normalizeVerb(selection,verbs):    
    for v in verbs:        
        if selection == v['v']:            
            return v['map']    
    return ""

def end_game(winning,points,moves):    
    if winning:        
        print('You have won! Congratulations')        
        print('You scored {points} points in {moves} moves! Nicely done!'.format(moves=moves, points=points))    
    else:        
        print('Thanks for playing!')        
        print('You scored {points} points in {moves} moves. See you next time!'.format(moves=moves, points=points))

def main():    
    gameFile = 'game.json'    
    
    game = {}    
    with open(gameFile) as json_file:        
        game = json.load(json_file)    
        current = 'START'    
        win = ['END']    
        lose = []    
        moves = 0    
        points = 0    
        inventory = []    
        areaInfo = True

    while True:  
        render(game,current,moves,points, areaInfo) 
        r = game['rooms']    
        c = r[current] 
        if c['name'] != 'skip':
            moves += 1
            
        selection = getInput(game,current,game['verbs'])        
        
        if selection is not None and selection[0] == 'QUIT':           
            end_game(False,points,moves)            
            break        
        
        areaInfo = True
        target = update(selection,game,current,inventory)
        
        if target[1] == False:
            current = target[0]
        if target[0] == 'JUSTTEXT' or target[1] == False:
            areaInfo = False
        else:
            current = target[0]
           

        if current in win:            
            end_game(True,points,moves)            
            break       
        
        if current in lose:            
            end_game(False,points,moves)            
            break
        



#if we are running this from the command line, run main
if __name__ == '__main__':
	main()