# Quick trading game
# v0.2.9
# Sir Aaron Burton
# Copyright - Please give me credit if you use this.

import time, random

#Player stuff
inv = []  #inventory (empty at first)
hp = 10   #health (doesn't do anything yet)
monies = 1000
upgrades = []
moniesHistory = []  #track the players worth over the game (for end game graph)
invHistory = []     #track the value of their inventory

#World stuff
worlds = ['earth','pluto','saturn',
          'forest moon of endor','alderaan','mustafar','hoth','dagobah','naboo','coruscant','tatooine','kashyyyk',
          'pandora','vulcan','deep space 9','krypton','scadrial','reach','harvest','onyx',
          'raxacoricofallapatorius','apalapucia',"demon's run",'skaro',
          'gargantua','cooper station','miller','edmunds',
          'gallifrey','sontar','trenzalore',
          'typhon','terra 2','harmony','hollow bastion','nobook',
          'ego','vormir','xandar','sakaar','asgard','nidavellir',
          'lusitania','shakesphere','path',
          'magrathea','betelgeuse v','vogsphere','damogran','sqornshellous zeta',
          'irk','vort','blorch','foodcourtia','conventia',
          'ludus','chthonia','frobozz']
random.shuffle(worlds)  #shuffle the order of the worlds for each game
day = 0
earth = worlds.index('earth') #locate earth
loc = earth #always start on earth
# Choose 3 random worlds to have a shop for ship upgrades
shops = [worlds.index(random.choice(worlds)) for i in range(30)]
# Include Earth as a "ship upgrade planet"
shops.append(earth)


#Item stuff
#Names of items for sale
#(you can add more if you want)
items = ['triangles',
         'hexagons',
         'trapezoids',
         'circles',
         'parallelograms',
         'tetracontadigrams',
         ]
#Default prices of items for sale
#This must have the same number of items as the items list has
default = [5,25,100,250,500,1000]
prices = default[:]


#Creating a function to make sure any inputs are numbers.
#I take a lot of number inputs, so this will be helpful
def numberInput(text=""):
    cow = input(text)
    while not cow.isdigit():
        print("Please enter a number:")
        cow = input(text)
    return int(cow)

def generatePrices():
    #randomly choose a price between 80% and 120% of the base price
    #0.4 is the spread, 120%-80%=40%  -->  40%=0.40
    #0.8 is the low end of the range, 80%=0.80
    #add 1% for each planet distance away from earth (0.01)
    #This makes the prices generally lower as you travel in one direction,
    #and higher as you travel the other.  Generally.  Random still applies.
    global prices
    for i in range(len(items)):
        newPrice = random.random()*default[i]*0.4 + default[i]*(0.8+0.01*(loc-earth))
        prices[i] = round(newPrice,2)

def showPrices():
    for i in range(len(items)):
        print('$%7.2f %s' %(prices[i],items[i].title()))
    print()

def storageSpace():
    return (100 + 100 * upgrades.count('cargo')) * (1 + 0.2 * upgrades.count('expandedCargo'))

def buy():
    #global means to use the variables defined before the function in the function.
    #It isn't always the best way to do it, but it is typicaly a quick solution.
    global monies, inv
    storage = storageSpace()
    print("What would you like to buy?")
    print("You have $%.2f monies." %(monies))
    for i in range(len(items)):
        print('%2i) $%7.2f %s' %(i+1,prices[i],items[i].title()))
    print(' 0) Nevermind')
    choice = numberInput()
    if choice == 0 or choice > len(items): return
    print()
    print("How many %s would you like to buy?" %(items[choice-1]))
    # using // for dividing instead of / forces the ansewr to be an integer (whole number)
    limit = monies//prices[choice-1]
    print("You can afford %i." %(limit))
    print("You have %i inventory space remaining." %(storage-len(inv)))
    purchase = numberInput()
    if purchase > limit:
        print("You cannot afford that many.")
        return
    for i in range(purchase):
        inv.append(items[choice-1])
        monies -= prices[choice-1]
    print("You bought %i %s for $%.2f monies." %(purchase,items[choice-1],prices[choice-1]*purchase))
    time.sleep(1)
    if len(inv) > storage:
        print("You cannot hold that many items.")
        print("You randomly dropped %i shapes." %(len(inv)-storage))
        random.shuffle(inv)
        inv = inv[0:storage]
        time.sleep(1)

def sell():
    global monies,inv
    print("What would you like to sell?")
    
    for i in range(len(items)):
        if items[i] in inv:
            print("%2i) $%7.2f %3i: %s" %(i+1,prices[i],inv.count(items[i]),items[i].title()))
    print(" 0) Nevermind")
    choice = numberInput()
    print()
    if choice == 0 or choice > len(items): return
    print("How many %s would you like to sell?" %(items[choice-1]))
    sale = numberInput()
    if sale > inv.count(items[choice-1]):
        print("You don't have that many.")
        time.sleep(1)
        return
    for i in range(sale):
        inv.remove(items[choice-1])
        monies += prices[choice-1]
    print("You sold %i %s for $%.2f monies." %(sale,items[choice-1],prices[choice-1]*sale))
    time.sleep(1)


def view():
    print('You currently have %.2f monies' %(monies))
    for item in items:
        print('%3i: %s' %(inv.count(item), item.title()))


def upgrade():
    global monies
    print("What would you like to upgrade?")
    print("You have %.2f monies" %(monies))
    # Engines start at $500, and go up 4x the price each upgrade
    engine = 500 * (3 ** upgrades.count('engine'))
    if 'brokenEngine' in upgrades: engine = 250
    # Storage always costs $1000
    storage = 1000
    # Shields are cheap at first, and increase exponentially as you get to 100
    # This is because they are % effective
    # This is a silly math equation.
    x = upgrades.count('shield')
    shields = 1000/(99-x) + 10*x
    # Weapons upgrade similar to engines, but steeper
    weapons = 1000 * (5 ** upgrades.count('weapon'))
    # If we are not on earth, alter the upgrade cost
    if loc != earth:
        priceScale = 2/max(shops.count(loc),1)
        engine *= priceScale
        storage *= priceScale
        shields *= priceScale
        weapons *= priceScale
    if 'brokenEngine' in upgrades:
        print(" 1) Repair Engine \t$%.2f" %(engine))
    else:
        print(" 1) Engine \t$%.2f" %(engine))
    print(" 2) Cargo Bay \t$%.2f" %(storage))
    print(" 3) Shields \t$%.2f" %(shields))
    print(" 4) Weapons \t$%.2f" %(weapons))
    print(" 0) Nevermind")
    
    choice = numberInput()
    if choice == 1:
        if monies >= engine:
            if 'brokenEngine' in upgrades:
                upgrades.remove('brokenEngine')
                print("Engine repaired!")
                return
            upgrades.append('engine')
            monies = monies - engine
            print("Engine upgraded!")
        else:
            print("You do not have enough monies.")
    elif choice == 2:
        if monies >= storage:
            upgrades.append('cargo')
            monies = monies - storage
            print("Cargo Bay Expanded to %i!" %(storageSpace()))
        else:
            print("You do not have enough monies.")
    elif choice == 3:
        if monies >= shields:
            upgrades.append('shield')
            monies = monies - shields
            print("Shields are now %i%% effective!" %(x+1))
        else:
            print("You do not have enough monies.")
    elif choice == 4:
        if monies >= weapons:
            upgrades.append('weapon')
            monies = monies - weapons
            print("You now have Level %i Weaponry!" %(upgrades.count('weapon')))
    elif choice == 0:
        return
    else:
        print("Unknown command")
    time.sleep(1)
    print()


def travel():
    global worlds, day
    travelDistance = 2 + upgrades.count('engine') - upgrades.count('brokenEngine')
    if travelDistance <=0:
        print("You are stuck here until you repair your engines.")
        print("You hail an emergency traveling merchant.")
        upgrade()
        day += 1
        return loc
    lowWorld = max(0,loc-travelDistance)
    highWorld = min(len(worlds),loc+travelDistance+1)
    availableWorlds = worlds[lowWorld:highWorld]
    print('Where would you like to go?')
    for i in range(len(availableWorlds)):
        print('%2i) %s' %(i+1,availableWorlds[i].title()))
    goto = input()
    while goto.isdigit() == False or int(goto)-1 >= len(availableWorlds):
        print('Please type the number of the planet:')
        goto = input()
    goto = availableWorlds[int(goto)-1]
    print()
    print('Traveling to %s...' %(goto.title()))
    print()
    day += 1
    time.sleep(1)
    return worlds.index(goto)

def menu():
    global loc, monies
    print(' 1) View Inventory')
    print(' 2) Buy Shapes')
    print(' 3) Sell Shapes')
    if loc in shops:
        print(' 4) Ship upgrades')
    print(' 0) Leave %s' %(worlds[loc].title()))

    option = numberInput()
    print()
    if option == 1:
        view()
    elif option == 2:
        buy()
    elif option == 3:
        sell()
    elif option == 0:
        old = loc
        loc = travel()
        moniesHistory.append(monies)
        invHistory.append(invValue())
        if old != loc:
            generatePrices()
        else:
            print("You wasted a day.")
        randomEvents()  #Initiate possible random events
    elif option == 4 and loc in shops:
        upgrade()
    elif option == 42:
        monies += 10000
    elif option == 333:
        global day
        day -= 10
    else:
        print("Unknown command")
    return option


def randomEvents():
    global prices, monies, inv, loc, worlds
    event = random.random()
    item = random.choice(items)
    #rare events come first, the low end of the random
    if event <= 0.07:
        #find random items  (less when the item is more expensive)
        quantity = random.randint(1,(6-items.index(item))*3)
        storage = storageSpace()
        print("You found %i random %s floating in space!" %(quantity,item))
        if len(inv)+quantity > storage:
            quantity = storage-len(inv)
            print("However, your inventory is too full, so you could only collect %i." %(quantity))
        for i in range(quantity):
            inv.append(item)
    elif event <= 0.11:
        #Worm Hole
        print("You got sucked into a wormhole,")
        loc = worlds.index(random.choice(worlds))
        #loc = random.randint(0,len(worlds)-1)
        print("you have arrived at %s." %(worlds[loc].title()))
    elif event <= 0.15:
        #Distress signal
        distressSignal()
    #more common events down here
    elif event >= 0.8:
        #price drop
        things = ["The %s miners worked extra hard" %(item),
                  "The %s's government has subsidized the %s" %(worlds[loc].title(),item[:-1]),
                  "%s says %s aren't cool" %(random.choice(['Bob Ross','John Cena','Steve']),item),
                  "%s spotted on a stale meme" %(item[:-1].capitalize()),
                  "For no reason at all"
                  ]
        print("%s, %s price drops." %(random.choice(things),item))
        which = items.index(item)
        prices[which] = prices[which]/2
    elif event >= 0.7:
        #price up
        #add some random things that might increase the price
        print("Thing happened, %s price increased." %(item))
        which = items.index(item)
        prices[which] *= 2
    elif event >= 0.6:
        #Space Pirates, give shapes or monies?
        spacePirates()
    elif event >= 0.5:
        print("A traveling merchant offeres to work on your ship.")
        upgrade()
    #add more events later
    #include at least one that give you things

def distressSignal():
    print("You received a distress signal.")
    print(" 1) Follow it")
    print(" 2) Ignore it")
    choice = numberInput()
    if choice == 1:
        print('You follow the distress signal, trying to help someone in need.')
        if random.random() < 0.33:
            spacePirates()
            # They were space pirates in disguise!
            return
        print("It looks like they have run out of Engine Juice.")
        # Add more random things they could have problems with
        print(" 1) Offer some of yours")
        print(" 2) Inquire about their mission")
        print(" 3) Peek at their inventory")
        print(" 4) Attack their ship")
        print(" 0) Abandon the needy")
        choice = numberInput()
        if choice == 1:
            print("They graciously accept your offer!")
            print("Now a fully functioning ship again, they want to return the favor.")
            print("Their ship mechanic has new technology to expand your inventory by 20%")
            print("They install it on your ship.  Its super effective!")
            upgrades.append('expandedCargo')
        elif choice == 2:
            print("They begin some long winded explanation about galactic peace and whatnot.")
            print("You leave while they are still talking.")
            #Do something more with this
        elif choice == 3:
            print("Whoa!  They get quite offended that you are looking at their stash.")
            #Random options
            #It is huge!
            #It is pathetic
        elif choice == 4:
            print('attack!')
            if fight():
                print('You win, loot their ship')
                print("doesnt work yet")
            else:
                print('You lost, to a distressed ship.')
                print("not implemented yet")
        else:
            print("You shamefully fly away.")
    else:
        print("You ignore the distress signal.")
        print("Hopefully they will be ok.")


def spacePirates():
    global monies, inv, hp
    print("Space Pirates attack you!")
    if  upgrades.count('shield') > random.randint(0,100):
        print("Your shields held them off.  You are safe for now.")
        return
    print("The Space Pirates demand 1/4 of your shapes, or 1/4 of your monies.")
    print("Give them:")
    print(" 1) $%.2f" %(monies/4))
    print(" 2) %i random shapes" %(len(inv)//4))
    print(" 3) Fight back!")
    print(" 4) Run away!")
    choice = numberInput()
    if choice == 1:
        print("You sigh and hand over the monies.")
        monies -= monies/4
    elif choice == 2:
        print("You open the doors to your cargo bay.")
        random.shuffle(inv)  #Shuffle your carago
        pirates = inv[:len(inv)//4] #pirates get the first half
        inv = inv[len(inv)//4:] #You get the second half
        #show what they took
        print("They took")
        for item in items:
            print('%3i: %s' %(pirates.count(item), item.title()))
    elif choice == 3:
        # Weapons come in to play here
        # earn something for winning the fight
        if fight():
            print('You win the fight!')
            print("You take their monies.")
            winnings = 80000//(100*random.random() +8)
            print("$%.2f" %(winnings))
            monies += winnings
            return
        else:
            print("They take half of your inventory for trying.")
            pirates = inv[:len(inv)//2] #pirates get the first half
            inv = inv[len(inv)//2:] #You get the second half
            #show what they took
            print("They took")
            for item in items:
                print('%3i: %s' %(pirates.count(item), item.title()))
    #elif choice == 4:
    else:
        if upgrades.count('engine') >= random.randint(0,3):
            print("You got away.")
            return
        print("The Space Pirates caught up with you.")
        print("They damage your ship.")
        print("They sabatoge your engines so you won't try that again.")
        print("Then, for good measure, they also steal half your monies.")
        if 'engine' in upgrades: upgrades.remove('engine')
        upgrades.append('brokenEngine')
        hp -= 1
        monies /= 2

#make a figh function
def fight():
    # Enemy ship has a random weapon quantity
    # Continue firing back and forth until someone runs out or looses all HP
    # Most shots do 1 damage.  Some can do 2, some 3
    # Shields block the shot.
    # Return True for victory, False for Defeat
    # (For now, you win if you have any weapons)
    if upgrades.count('weapon'):
        print("You engage in an epic battle in which you have no actual control.")
        time.sleep(1)
        enemyHP = 5
        # The enemy has a 2/3 chance to have level 1 weapons.
        enemyRandom = random.randint(1,9)
        if enemyRandom <= 6: enemyWeapon = 1
        elif enemyRandom <= 8: enemyWeapon = 2
        else: enemyWeapon = 3
        enemyShield = 3/(100*random.random()+3)
        print("Wow!  Their shields are %i%% effective!" %(enemyShield*100))
        time.sleep(1)
        global hp #bring your current health along for the ride
        yourWeapon = upgrades.count('weapon')
        yourShield = upgrades.count('shield')/100
        print("Both ships fire a volley of shots.")
        time.sleep(1)
        while enemyHP > 0 and hp > 0:
            if random.random() < enemyShield:
                print("Your shot was blocked by the enemies shield.")
            else:
                print("You hit the enemy and did %i damage to their hull." %(yourWeapon))
                enemyHP -= yourWeapon
            print("The enemy has %i HP" %(enemyHP))
            time.sleep(1)
            if enemyHP <=0: break
            if random.random() < yourShield:
                print("The enemies shot was blocked by your shield.")
            else:
                print("The enemy hit you and did %i damage to your hull." %(enemyWeapon))
                hp -= enemyWeapon
            print("You have %i HP" %(hp))
            time.sleep(1)
        if hp > 0:
            return True
    else:
        print("You have nothing to fight with.")
    return False

#Convert inventory to value on current planet at current prices
#This is for information and making cool graphs later
def invValue():
    global prices,inv,items
    total = 0
    for i in range(len(items)):
        total += prices[i] * inv.count(items[i])
    return total


#Draw a text based graph of your monies history
def drawGraph(tall=10):
    liquid = [moniesHistory[i] + invHistory[i] for i in range(len(invHistory))]
    row = [' ']*33
    graph = []
    for i in range(tall+2):
        graph.append(row[:])

    for row in graph:
        row[1] = '|'

    for i in range(len(liquid)):
        height = int((tall*moniesHistory[i])//max(liquid))
        graph[tall-height][i+2] = '$'
        height = int((tall*invHistory[i])//max(liquid))
        graph[tall-height][i+2] = 'I'
        height = int((tall*liquid[i])//max(liquid))
        graph[tall-height][i+2] = '*'
        graph[tall+1][i+2] = '_'

    graph[0].append('$%.2f' %(max(liquid)))

    for row in graph:
        print(''.join(row))


while day <= 30:
    print()
    print('Day',day,'on',worlds[loc].title())
    print('You have $%.2f monies.' %(monies))
    print()
    showPrices()
    #time.sleep(1) 
    #buy/sell stuff
    option = menu()
    if hp <= 0:
        print("Your ship is damaged beyond repair.  You loose.")
        break

drawGraph(15)        
print("You have run out of day.")
print("You have $%.2f" %(monies))
print()
input('Press ENTER to quit')
