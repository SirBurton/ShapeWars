# January 2021
# Sir Burton
# Shapewars as a GUI?
# v0.3.3

from tkinter import *
from tkinter import simpledialog, messagebox
import time, random
from functools import partial

window = Tk()
window.title("ShapeWars")
textFont = ("Courier",12)

#Player stuff
inv = []  #inventory (empty at first)
hp = 10   #health
monies = 1000
upgrades = []
moniesHistory = []  #track the players worth over the game (for end game graph)
invHistory = []     #track the value of their inventory

#World stuff
worlds = ['Earth','Pluto','Saturn',
          'Forest Moon of Endor','Alderaan','Mustafar','Hoth','Dagobah','Naboo','Coruscant','Tatooine','Kashyyyk',
          'Pandora','Vulcan','Deep Space 9','Krypton','Scadrial','Reach','Harvest','Onyx',
          'Raxacoricofallapatorius','Apalapucia',"Demon's Run",'Skaro','Gallifrey','Sontar','Trenzalore',
          'Gargantua','Cooper station','Miller','Edmunds',
          'Typhon','Terra 2','Harmony','Hollow Bastion','Nobook',
          'Ego','Vormir','Xandar','Sakaar','Asgard','Nidavellir',
          'Lusitania','Shakesphere','Path',
          'Magrathea','Betelgeuse V','Vogsphere','Damogran','Sqornshellous Zeta',
          'Irk','Vort','Blorch','Foodcourtia','Conventia',
          'Ludus','Chthonia','Frobozz']
random.shuffle(worlds)  #shuffle the order of the worlds for each game
day = 0
earth = worlds.index('Earth') #locate earth
loc = earth #always start on earth
# Choose 30 ish random worlds to have a shop for ship upgrades
shops = [worlds.index(random.choice(worlds)) for i in range(30)]
# Include Earth as a "ship upgrade planet
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
        displayPrices[i].config(text='$%.2f' %(prices[i]))

def updateMoniesDisplay():
    moneyLabel.config(text='You have $%.2f Monies' %(monies))

def storageSpace():
    return int((100 + 100 * upgrades.count('cargo')) * (1 + 0.2 * upgrades.count('expandedCargo')))

def buy(item):
    #global means to use the variables defined before the function in the function.
    #It isn't always the best way to do it, but it is typicaly a quick solution.
    global monies, inv
    storage = storageSpace()
    text1 = "How many %s would you like to buy?" %(items[item])
    # using // for dividing instead of / forces the ansewr to be an integer (whole number)
    limit = monies//prices[item]
    text2 = "You can afford %i." %(limit)
    text2 += "\nYou have %i inventory space remaining." %(storage-len(inv))
    purchase = simpledialog.askinteger(title=text1, prompt=text2)
    if not purchase: return
    purchase = int(purchase)
    if purchase > limit:
        messagebox.showwarning(title="whoops",message="You cannot afford that many.")
        return
    for i in range(purchase):
        inv.append(items[item])
        monies -= prices[item]
    if len(inv) > storage:
        text = "You cannot hold that many items."
        text += "\nYou randomly dropped %i shapes." %(len(inv)-storage)
        messagebox.showerror(title="Oops.",message=text)
        random.shuffle(inv)
        inv = inv[0:storage]
    displayInvs[item].config(text=inv.count(items[item]))
    updateMoniesDisplay()

def sell(item):
    global monies,inv
    text1 = 'How many %s?' %(items[item])
    text2 = 'You have %i %s' %(inv.count(items[item]),items[item])
    sale = simpledialog.askinteger(title=text1, prompt=text2)
    if not sale: return
    sale=int(sale)
    if sale > inv.count(items[item]):
        messagebox.showwarning(title="whoops",message="You don't have that many.")
        return
    for i in range(sale):
        inv.remove(items[item])
        monies += prices[item]
    displayInvs[item].config(text=inv.count(items[item]))
    updateMoniesDisplay()


def upgradeBox():
    box = Toplevel(window)
    box.title("Upgrade Shop!")
    Label(box, text='What would you like to upgrade?').grid(row=0, column=0, columnspan=5)
    mon = Label(box, text="You have %.2f monies" %(monies))
    mon.grid(row=1, column=0, columnspan=5)
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
        button1 = Button(box,text="Repair Engine \n$%.2f" %(engine),command=partial(upgrade,1,engine,box), width=10)
    else:
        button1 = Button(box,text="Engine \n$%.2f" %(engine),command=partial(upgrade,1,engine,box), width=10)
    button2 = Button(box,text="Cargo Bay \n$%.2f" %(storage),command=partial(upgrade,2,storage,box), width=10)
    button3 = Button(box,text="Shields \n$%.2f" %(shields),command=partial(upgrade,3,shields,box), width=10)
    button4 = Button(box,text="Weapons \n$%.2f" %(weapons),command=partial(upgrade,4,weapons,box), width=10)
    button5 = Button(box,text="Leave\nShop", command=box.destroy, width=10)

    button1.grid(row=3, column=0)
    button2.grid(row=3, column=1)
    button3.grid(row=3, column=2)
    button4.grid(row=3, column=3)
    button5.grid(row=3, column=4)
    
def upgrade(choice,cost,box):
    global monies
    if choice == 1:
        if monies >= cost:
            if 'brokenEngine' in upgrades:
                upgrades.remove('brokenEngine')
                messagebox.showinfo(message="Engine repaired!")
                return
            upgrades.append('engine')
            monies = monies - cost
            messagebox.showinfo(message="Engine upgraded to level %i!" %(upgrades.count('engine')+1),parent=window)
            travelButtons(travelFrame)
        else:
           messagebox.showinfo(message="You do not have enough monies.")
    elif choice == 2:
        if monies >= cost:
            upgrades.append('cargo')
            monies = monies - cost
            messagebox.showinfo(message="Cargo Bay Expanded to %i!" %(storageSpace()))
        else:
            messagebox.showinfo(message="You do not have enough monies.")
    elif choice == 3:
        if monies >= cost:
            x = upgrades.count('shield')
            upgrades.append('shield')
            monies = monies - cost
            messagebox.showinfo(message="Shields are now %i%% effective!" %(x+1))
        else:
            messagebox.showinfo(message="You do not have enough monies.")
    elif choice == 4:
        if monies >= cost:
            upgrades.append('weapon')
            monies = monies - cost
            messagebox.showinfo(message="You now have Level %i Weaponry!" %(upgrades.count('weapon')))
        else:
            messagebox.showinfo(message="You do not have enough monies.")
    box.destroy()
    updateMoniesDisplay()


def travelButtons(frame):
    global worlds
    # remove old buttons
    olds = frame.slaves()
    for old in olds:
        old.destroy()
    if shops.count(loc):
        upgradeButton.grid()
    else: upgradeButton.grid_forget()
    if day >= 30:  #game over
        Label(frame,text="you have run out of day").pack()
        return
    travelDistance = 2 + upgrades.count('engine') - upgrades.count('brokenEngine')
    '''if travelDistance <=0:
        print("You are stuck here until you repair your engines.")
        print("You hail an emergency traveling merchant.")
        upgrade()
        day += 1
        return loc'''
    lowWorld = max(0,loc-travelDistance)
    highWorld = min(len(worlds),loc+travelDistance+1)
    availableWorlds = worlds[lowWorld:highWorld]
    offset = availableWorlds.index(worlds[loc])
    buttons = []
    for i in range(len(availableWorlds)):
        buttons.append(Button(frame, text=availableWorlds[i],command=partial(travel,i-offset)))
    for button in buttons:
        button.pack(side=LEFT)

def travel(where):
    global loc, day
    loc += where
    day += 1
    generatePrices()
    randomEvents()
    dayLabel.config(text='Day %i on %s' %(day,worlds[loc]))
    travelButtons(travelFrame)
    

def randomEvents():
    global prices, monies, inv, loc, worlds
    event = random.random()
    item = random.choice(items)
    names = ['Bob Ross','John Cena','Steve','Denzel Washington','Edgar Allan Poe','Clint Eastwood',
             'Leonardo da Vinci','Tom Cruise', 'Lady Gaga', 'Marilyn Monroe']
    #rare events come first, the low end of the random
    if event <= 0.07:
        #find random items  (less when the item is more expensive)
        quantity = random.randint(1,(6-items.index(item))*3)
        storage = storageSpace()
        text = "You found %i random %s floating in space!" %(quantity,item)
        if len(inv)+quantity > storage:
            quantity = int(storage-len(inv))
            text += "\nHowever, your inventory is too full, so you could only collect %i." %(quantity)
        for i in range(quantity):
            inv.append(item)
        messagebox.showinfo("Good news!",text)
        displayInvs[items.index(item)].config(text=inv.count(item))
    #elif event <= 0.11:
    #    #Worm Hole
    #    print("You got sucked into a wormhole,")
    #    loc = worlds.index(random.choice(worlds))
    #    #loc = random.randint(0,len(worlds)-1)
    #    print("you have arrived at %s." %(worlds[loc]))
    #elif event <= 0.15:
    #    #Distress signal
    #    distressSignal()
    #more common events down here
    
    elif event >= 0.8:
        #price drop
        things = ["The %s miners worked extra hard." %(item),
                  "The %s's government has subsidized the %s." %(worlds[loc],item[:-1]),
                  "%s says %s aren't cool." %(random.choice(names),item),
                  "%s spotted on a stale meme." %(item[:-1].capitalize()),
                  "For no reason at all."
                  ]
        messagebox.showinfo("%s price drops" %(item),random.choice(things))
        which = items.index(item)
        prices[which] = prices[which]/2
        displayPrices[which].config(text='$%.2f' %(prices[which]))
    elif event >= 0.7:
        #price up
        things = ["The %s miners went on strike." %(item),
                  "The %s's government has placed a tarrif on the %s" %(worlds[loc],item[:-1]),
                  "%s says %s are super cool." %(random.choice(names),item),
                  "%s spotted on a dank meme." %(item[:-1].capitalize()),
                  "For some strange reason."
                  ]
        messagebox.showinfo("%s price incresed" %(item),random.choice(things))
        which = items.index(item)
        prices[which] *= 2
        displayPrices[which].config(text='$%.2f' %(prices[which]))
    #elif event >= 0.6:
        #Space Pirates, give shapes or monies?
    #    spacePirates()
    #elif event >= 0.5:
    #    print("A traveling merchant offeres to work on your ship.")
    #    upgrade()
    #add more events later
    #include at least one that give you things

def distressSignal():
    print("You received a distress signal.")
    print(" 1) Follow it")
    print(" 2) Ignore it")
    choice = numberInput()
    if choice == 1:
        print('You follow the distress signal, trying to help someone in need.')
        if random.random() < 0.3:
            print("They were Space Pirates in disguise!")
            spacePirates()
            return
        print("They need some help repairing a thing on their ship.")
        # Add more random things they could have problems with
        print(" 1) Offer to help")
        print(" 2) Inquire about their mission")
        print(" 3) Peek at their inventory")
        print(" 4) Attack their ship")
        print(" 0) Abandon the needy")
        choice = numberInput()
        if choice == 1:
            print("They graciously accept your offer!")
            time.sleep(1)
            print("That took 1 day.")
            time.sleep(1)
            global day
            day += 1
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
            print("eventually this will have some consequences.")
            #Random options
            #It is huge!
            #It is pathetic
        elif choice == 4:
            print('attack!')
            if fight():
                global monies
                print('You win, loot their ship')
                print('You win the fight!')
                print("You take their monies.")
                winnings = loot()
                print("$%.2f" %(winnings))
                monies += winnings
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
            winnings = loot()
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

#How much monies you get when winning a fight
def loot(level = 1):
    return (level * 80000)//(100*random.random() +8)

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

'''
while day <= 30:
    if hp <= 0:
        print("Your ship is damaged beyond repair.  You loose.")
        break
'''
dayLabel = Label(window,text='Day %i on %s' %(day,worlds[loc]))
dayLabel.grid(row=1,column=2,columnspan=1)
moneyLabel = Label(window,text='You have $%.2f Monies' %(monies))
moneyLabel.grid(row=2,column=2)

displayPrices = []
buyButtons = []
shapeLabels = []
sellButtons = []
displayInvs = []

for i in range(len(items)):
    displayPrices.append(Label(window,text='$%.2f' %(prices[i]),font=textFont))
    displayPrices[i].grid(row=i+3, column=0)
    buyButtons.append(Button(window,text="Buy",command=partial(buy,i)))
    buyButtons[i].grid(row=i+3,column=1)
    shapeLabels.append(Label(window,text=items[i].title(), font=textFont))
    shapeLabels[i].grid(row=i+3, column=2)
    sellButtons.append(Button(window,text="Sell",command=partial(sell,i)))
    sellButtons[i].grid(row=i+3,column=3)
    displayInvs.append(Label(window,text=inv.count(items[i]),font=textFont))
    displayInvs[i].grid(row=i+3,column=4)

upgradeButton = Button(window,text="Upgrades", command=upgradeBox)
upgradeButton.grid(row=len(items)+5, column=0)

travelFrame = Frame(window, bg='#222244')
travelFrame.grid(row=len(items)+4,column=0, columnspan=6, sticky='we')
travelButtons(travelFrame)

window.mainloop()
