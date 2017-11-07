import os
import random
from sqlite3 import connect

import Armor
import Enemy
import Hero
import Shield
import Weapon
import Item


# One round of a battle
def battle():
    ourHero.printheroinfo()

    print('[a]tk, [d]ef, [r]un\n')
    nextmove = input()
    playerturn(nextmove)
    enemyturn()
    if not ourHero.isalive():
        isbattling = False
        print('YOU DIED')
        quit()
    if not ourEnemy.isalive():
        isbattling = False
        ourEnemy.reset()
        print('VICTORY')
        print('You gained ' + str(ourEnemy.xp) + ' EXP')
        ourHero.xp += ourEnemy.xp
        if ourHero.xp > ourHero.nextlevel:
            ourHero.levelup()
        camp()
    pass


def playerturn(m):
    crit = 0
    critchance = random.randrange(0, 31)
    if critchance == 0:
        crit = ourHero.atk * .5
    effatk = ourHero.atk + crit - ourEnemy.defn
    if m == 'a':
        if critchance == 0:
            print('CRITICAL HIT!')
        print('Player attacks Enemy for ' + str(effatk))
        ourEnemy.hp = ourEnemy.hp - effatk
    if m == 'd':
        ourHero.defn += ourHero.defn * .2
    if m == 'r':
        rand = random.randrange(0, 4)
        if rand == 0:
            print('you ran away')
            isbattling = False
            return
        else:
            print('you can\'t run!')


def getenemy():
    conn.execute('SELECT * FROM enemies WHERE level = ' + str(ourHero.level) + ';')
    rows = conn.fetchall()
    new_enemy = random.choice(rows)
    # create random enemy name
    adjectives1 = random.choice((rows[0][2], rows[1][2], rows[2][2], rows[3][2], rows[4][2]))
    adjectives2 = random.choice((rows[0][3], rows[1][3], rows[2][3], rows[3][3], rows[4][3]))
    ourNewEnemy = Enemy.Enemy(new_enemy[0], adjectives1, adjectives2, new_enemy[3], new_enemy[4], new_enemy[5],
                              new_enemy[6], new_enemy[7], new_enemy[8], new_enemy[9])
    return ourNewEnemy


def newhero():
    conn.execute('SELECT * FROM levelnotes WHERE level = 1;')
    rows = conn.fetchall()

    print('[w]arrior, [m]age, [h]unter')
    ourclass = input()
    if ourclass == 'w':
        ourclass = 'Warrior'
    elif ourclass == 'm':
        ourclass = 'Mage'
    elif ourclass == 'h':
        ourclass = 'Hunter'

    new_hero_data = rows[0]
    ournewhero = Hero.Hero(ourclass, new_hero_data[0], new_hero_data[1], new_hero_data[2], new_hero_data[3],
                           new_hero_data[4])
    return ournewhero


def newweapon():
    conn.execute('SELECT * FROM weapons where level = ' + str(ourHero.level) + ';')
    rows = conn.fetchall()
    new_weapon_data = rows[0]
    ournewweapon = Weapon.Weapon(new_weapon_data[0], new_weapon_data[1], new_weapon_data[2], new_weapon_data[3],
                                 new_weapon_data[4])
    return ournewweapon


def newarmor():
    conn.execute('SELECT * FROM armor WHERE "level" = ? AND "classtype" = ? ;', (str(ourHero.level), str(ourHero.ourclass), ))
    rows = conn.fetchall()
    new_armor_data = rows[0]
    ournewarmor = Armor.Armor(new_armor_data[0], new_armor_data[1], new_armor_data[2], new_armor_data[3],
                              new_armor_data[4])
    return ournewarmor


def newshield():
    conn.execute('SELECT * FROM shields WHERE "level" = ? AND "class" = ? ;', (str(ourHero.level), str(ourHero.ourclass), ))
    rows = conn.fetchall()
    new_shield_data = rows[0]
    ournewshield = Shield.Shield(new_shield_data[0], new_shield_data[1], new_shield_data[2], new_shield_data[3],
                                 new_shield_data[4])
    return ournewshield


def newitem():
    conn.execute('SELECT * FROM items WHERE "grade" = ? ;', ('minor',))
    rows = conn.fetchall()
    new_item_data = rows[0]
    print(new_item_data)
    ournewitem = Item.Item(new_item_data[0], new_item_data[1], new_item_data[2], new_item_data[3])
    return ournewitem


def enemyturn():
    effatk = int(round(ourEnemy.atk - ourHero.defn, 1))
    if effatk < 0:
        effatk = 0
    print('\nEnemy Attacks Player for ' + str(effatk))
    ourHero.hp = ourHero.hp - effatk


def camp():
    ourHero.printheroinfo()
    print('you are now at camp')
    print('[r]est? [i]tem? [e]quip [a]dventure [l]oad [s]ave')
    m = input()
    if m == 'r':
        ourHero.hp = ourHero.maxhp
        return
    elif m == 'i':
        return
    elif m == 'e':
        inventory_management()
    elif m == 'a':
        adventure()
    elif m == 'l':
        inventory_management()
    elif m == 's':
        savegame()
    elif m == 'q':
        quit()


# pickle out to hero obj
def loadgame():
    pass


# pickle in to hero obj and start gameloop
def savegame():
    pass


def inventory_management():
    for i, item in enumerate(ourHero.heroitems):
        print('[' + i + '] - ' + item)
    pass


def gameloop():
    while True:
        adventure()


def adventure():
    print('[a]dventure or [c]amp')
    m = input()
    ourrand = random.randint(0, 100)
    if m == 'a':
        if ourrand <= 80:
            isbattling = True
            # Make new enemy
            ourEnemy = getenemy()
            print('\nYou are confronted by a ' + str(ourEnemy.name))
            # battle until one is dead
            ourEnemy.printenemyinfo()
            while ourHero.isalive() and ourEnemy.isalive() and isbattling:
                battle()
        if 80 < ourrand <= 85:
            print('\nYou couldn\'t find anything so you came back to camp')
            camp()
        if 85 < ourrand <= 95:
            print('You found an item!')
            pass
        if 95 < ourrand <= 100:
            print('You find a traveler,')
            pass
    elif m == 'c':
        camp()


# Create all game databases (only needs to run once to make databases)
# dbsetup.setup()

print('Welcome to MiniRPG\n\n')

# our database path
dbpath = './db/game.db'

# our boolean if battling
isbattling = False

# import and create our player database
gamedb = connect(dbpath)
conn = gamedb.cursor()

# Make new global hero and enemy which will change over time
ourHero = newhero()

# Make a basic weapon
ourHero.items[0] = newweapon()

# Make a basic armor
ourHero.items[1] = newarmor()

# Make a basic shield
ourHero.items[2] = newshield()

# Make a potion
ourHero.items[3] = newitem()

# make a basic enemy object
ourEnemy = getenemy()

gameloop()
