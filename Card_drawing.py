from dataclasses import dataclass
from tkinter import *
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageTk
from enum import Enum
import random
from gradient import linear_gradient
from collections import deque
import configparser
import json
import textwrap

class PokemonTypes(Enum):
    NORMAL = 1
    FIRE = 2
    WATER = 3
    GRASS = 4
    ELECTRIC = 5
    PSYCHIC = 6
    FIGHTING = 7
    DARK = 8
    STEEL = 9
    DRAGON = 10
    ROCK = 11
    POISON = 12
    ICE = 13
    BUG = 14
    GHOST = 15
    GROUD = 16
    FLYING = 17
    UNKNOWN = 18
    FAIRY = 19

GS = 'GillSans.ttf'
GSB = 'GillSans Bold.ttf'
GSEB = 'GillSansStd_ExtraBold.ttf'
FLTMBI = 'Futura-Bold-Italic.ttf'
# Futura LT medium bolditalic
GSCB = 'GillSans Condensed Bold.otf'
FPTH = 'Futura PT.ttf'
# Futura lt medium bold
FLTMB = 'FuturaLT-Bold.ttf'
fonts = [GS, GSB, GSEB, FLTMBI, GSCB, FPTH, FLTMB]
class Card:
    @dataclass #doesn't force anything
    class Attack:
        name: str
        description: str
        damage: int
        use_cost: [PokemonTypes]
    @dataclass
    class Info:
        number: int
        height: float
        weight: float

    def __init__(self):
        self.name = "MYC"
        self.type = [PokemonTypes.NORMAL,PokemonTypes.FLYING]
        self.evolves_from = "None"
        self.HP = 70
        self.info = self.Info(15, 100, 40)
        self.picture = self.name + ".jpg"
        self.attack1 = self.Attack("Egg Shot", "BOC shoots an egg at the opponent",
                                   2, [PokemonTypes.NORMAL])
        self.attack2 = self.Attack("Frightened charge", "You scared BOC and he'll be charging at you fast enough to break a wall!",
                                   3, [PokemonTypes.NORMAL,PokemonTypes.FIGHTING])
        self.weakness = [PokemonTypes.ICE]   
        self.resistance = [PokemonTypes.FIGHTING]
        self.retreat = [PokemonTypes.NORMAL, PokemonTypes.NORMAL]
##    def __init__(self, configFile):
##        config = configparser.ConfigParser()
##        config.read(configFile,encoding='utf8')
##        data = config['DEFAULT']
##        self.name = data['name']
##        # for name, member in PokemonTypes.__members__.items():
##        #     if name == data['type']:
##               # self.type = PokemonTypes[]
##        self.type = [PokemonTypes[energy] for energy in json.loads(data['type'])]
##        self.evolves_from = data['evolves_from']
##        self.HP = data['HP']
##        self.info = self.Info(data['number'], data['height'], data['weight'])
##        self.picture = data['picture']
##        self.attack1 = self.Attack(data['attack1_name'],data['attack1_description'],
##                              data['attack1_damage'],[PokemonTypes[energy] for energy in json.loads(data['attack1_use_cost'])])
##        self.attack2 = self.Attack(data['attack2_name'],data['attack2_description'],
##                              data['attack2_damage'],[PokemonTypes[energy] for energy in json.loads(data['attack2_use_cost'])])
##        self.weakness = [PokemonTypes[energy] for energy in json.loads(data['weakness'])]
##        self.resistance = [PokemonTypes[energy] for energy in json.loads(data['resistance'])]
##        self.retreat = [PokemonTypes[energy] for energy in json.loads(data['retreat'])]
    def write_config(self):
        config = configparser.ConfigParser()
        # config['name'] = self.name
        # config['type'] = self.type
        # config['evolves_from'] = self.evolves_from
        # config['HP'] = self.HP
        config['DEFAULT'] = {'name':self.name,
                             'type': json.dumps([i.name for i in self.type]),
                             'evolves_from': self.evolves_from,
                             'HP': self.HP,
                             'number':self.info.number,
                             'height':self.info.height,
                             'weight':self.info.weight,
                             'picture':self.picture,
                             'attack1_name':self.attack1.name,
                             'attack1_damage': self.attack1.damage,
                             'attack1_description': self.attack1.description,
                             'attack1_use_cost': json.dumps([i.name for i in self.attack1.use_cost]),
                             'attack2_name': self.attack2.name,
                             'attack2_damage': self.attack2.damage,
                             'attack2_description': self.attack2.description,
                             'attack2_use_cost': json.dumps([i.name for i in self.attack2.use_cost]),
                             'weakness': json.dumps([i.name for i in self.weakness]),
                             'resistance': json.dumps([i.name for i in self.resistance]),
                             'retreat': json.dumps([i.name for i in self.retreat])
                             }
        with open(self.name + '.ini', 'w', encoding='utf8') as configfile:
            ...
            config.write(configfile)

def paste_symbol(card, card_image, energies, coord):
    x_middle = coord[0] + 30
    x_start = x_middle - len(energies) * 30
    how_many = 0
    for energy in energies:
        how_many += 1
        symbol = Image.open(energy.name + ".png")
        # This keeps the scale, makes it "not bigger than"
        symbol.thumbnail((60, 60))
        # Pasting poke pic
        card_image.paste(symbol, (x_start, coord[1]), symbol)
        x_start += 60
def paste_symbol_from_left(card, card_image, energies, coord):
    x_start = coord[0]
    for energy in energies:
        symbol = Image.open(energy.name + ".png")
        # This keeps the scale, makes it "not bigger than"
        symbol.thumbnail((42, 42))
        # Pasting poke pic
        card_image.paste(symbol, (x_start, coord[1]), symbol)
        x_start += 42
def draw_name(card, card_image):
    d = ImageDraw.Draw(card_image)
    fnt = ImageFont.truetype(GSB, 50)
    d.text((150, 22), card.name, font=fnt, fill=(0,0,0))
def draw_HP_and_type(card, card_image):
    d = ImageDraw.Draw(card_image)
    HP_start_x = 535
    HP_start_y = 65
    fnt = ImageFont.truetype(GSEB, 15)
    d.text((HP_start_x, HP_start_y), "HP", font=fnt, fill=(0,0,0))

    fnt = ImageFont.truetype(FLTMB, 50)
    d.text((HP_start_x+30, HP_start_y-35), str(card.HP), font=fnt, fill=(0,0,0))

    paste_symbol(card, card_image, card.type, (HP_start_x+105, HP_start_y-35))
def draw_evolves(card, card_image):
    if card.evolves_from != "None":
        d = ImageDraw.Draw(card_image)
        fnt = ImageFont.truetype(FLTMBI, 24)
        d.text((130, 80), "Evolves from " + card.evolves_from, font=fnt, fill=(0,0,0))
def draw_Attack1(card, card_image):
    d = ImageDraw.Draw(card_image)
    fnt = ImageFont.truetype(FPTH, 50)
    attack_x_start = 195#calculate_x_of_attacks
    attack_y_start = 560

    paste_symbol_from_left(card, card_image, card.attack1.use_cost, (48, attack_y_start + 13))

    d.text((attack_x_start, attack_y_start), card.attack1.name, font=fnt, fill=(0,0,0))

    fnt = ImageFont.truetype(FPTH, 50)
    d.text((620, attack_y_start), str(card.attack1.damage), font=fnt, fill=(0,0,0))

    fnt = ImageFont.truetype(GS, 30)
    att_info = card.attack1.description
    print(len(att_info))
    if len(att_info) > 45:
        s = textwrap.fill(att_info, 45)
        print(s)
    d.text((55, attack_y_start + 62), card.attack1.description, font=fnt, fill=(0,0,0))
def draw_Attack2(card, card_image):
    d = ImageDraw.Draw(card_image)
    fnt = ImageFont.truetype(FPTH, 50)

    attack_x_start = 195  # calculate_x_of_attacks
    attack_y_start = 700

    paste_symbol_from_left(card, card_image, card.attack2.use_cost, (48, attack_y_start+13))

    d.text((attack_x_start, attack_y_start), card.attack2.name, font=fnt, fill=(0,0,0))

    fnt = ImageFont.truetype(FPTH, 50)
    d.text((620, attack_y_start), str(card.attack2.damage), font=fnt, fill=(0,0,0))

    att_info = card.attack2.description
    print(len(att_info))
    if len(att_info) > 45:
        att_info = textwrap.fill(att_info, 45)
    fnt = ImageFont.truetype(GS, 30)
    d.text((55, attack_y_start + 62), att_info, font=fnt, fill=(0,0,0))
def draw_info(card, card_image):
    d = ImageDraw.Draw(card_image)
    fnt = ImageFont.truetype(GS, 24)
    d.text((240, 520), "#" + str(card.info.number) + " Высота: " +
           str(card.info.height) + " Вес: " + str(card.info.weight), font=fnt, fill=(0,0,0))
def draw_weakness(card, card_image):
    d = ImageDraw.Draw(card_image)
    fnt = ImageFont.truetype(GS, 24)
    y_start = 895
    x_start = 50
    d.text((x_start, y_start), "Слабость", font=fnt, fill=(0,0,0))
    paste_symbol(card, card_image, card.weakness, (x_start+20, y_start + 30))
def draw_resistance(card, card_image):
    d = ImageDraw.Draw(card_image)
    fnt = ImageFont.truetype(GS, 24)
    y_start = 895
    x_start = 280
    d.text((x_start, y_start), "Устойчивость", font=fnt, fill=(0,0,0))
    paste_symbol(card, card_image, card.resistance, (x_start + 40, y_start + 30))
def draw_run(card, card_image):
    d = ImageDraw.Draw(card_image)
    fnt = ImageFont.truetype(GS, 24)
    #type = card.retreat[0]
    #cost = card.retreat[1]
    y_start = 895
    x_start = 530
    d.text((x_start, y_start), "Отступление", font=fnt, fill=(0,0,0))
    paste_symbol(card, card_image, card.retreat, (x_start+40, y_start + 30))
def draw_text(card, card_image):
    draw_name(card, card_image)
    draw_HP_and_type(card, card_image)
    draw_evolves(card, card_image)
    draw_Attack1(card, card_image)
    draw_Attack2(card, card_image)
    draw_info(card, card_image)
    draw_weakness(card, card_image)
    draw_resistance(card, card_image)
    draw_run(card, card_image)

def draw_border(card_image):
    border_width = 20
    for x in range(card_image.width):
        for y in range(card_image.height):
            if (x < border_width
                    or y < border_width
                    or x > card_image.width - border_width - 1
                    or y > card_image.height - border_width - 1):
                card_image.putpixel((x, y), (210, 180, 56))
def draw_border_from(card_image, x_offset, y_top_offset, y_bottom_offset):
    border_width = 3
    for x in range(x_offset,card_image.width-x_offset):
        for y in range(y_top_offset,card_image.height-y_bottom_offset):
            if (abs(x-x_offset) < border_width
                    or abs(y-y_top_offset) < border_width
                    or x > card_image.width-x_offset - border_width - 1
                    or y > card_image.height-y_bottom_offset - border_width - 1):
                card_image.putpixel((x, y), (100, 100, 100))
def populate_card(card):
    #card.write_config()
    # creates a new empty image, RGB mode, and size 400 by 400.
    new_im = Image.new('RGB', (732,1032), (255, 255, 128))
    #new_im = Image.open("Pika.jpg")
    poke_pic = Image.open(card.picture)
    #colors = linear_gradient("#cfc376", "#b89f00",30)
    #rolling_colors = deque(colors)
    # for x in range(new_im.width):
    #     for y in range(new_im.height):
    #         new_im.putpixel((x, y), random.choice(colors))
    # for x in range(300,new_im.width):
    #     for y in range(500,new_im.height):
    #         r,g,b = new_im.getpixel((x,y))
    #         r = min(255, int(r*1.3))
    #         g = min(255, int(g * 1.3))
    #         b = min(255, int(b * 1.3))
    #         new_im.putpixel((x, y), (r,g,b))
    #         if (random.randint(1,10000)) % 10 == 0:
    #             rolling_colors.rotate(1)
    #         new_im.putpixel((x, y), rolling_colors[5])

            # new_im.putpixel((x, y),
            #                 colors[
            #     int( (len(colors)-1)*((7*y)%new_im.height)/new_im.height )
            # ])
    #new_im = new_im.filter(ImageFilter.MedianFilter(5))
    # This resizes the picture without keeping scale ratio
    poke_pic = poke_pic.resize((632,450))
    # This keeps the scale, makes it "not bigger than"
    # poke_pic.thumbnail((632,450))

    #Pasting poke pic
    new_im.paste(poke_pic, (50,100))

    # Writing all the text now
    draw_text(card, new_im)

    draw_border(new_im)
    draw_border_from(new_im, 20,20,20)
    draw_border_from(new_im, 50, 100,480)
    draw_border_from(new_im, 40, 890, 140)
    #new_im.show()
    new_im.save("card_from_python.jpg")
#print(json.dumps(['ELECTRIC']))
# config = configparser.ConfigParser()
# config.read("example.ini", encoding='utf8')
# data=config['DEFAULT']
# p = PokemonTypes[json.loads(data['type'])[0]]
# print(PokemonTypes.ELECTRIC)

#pikachu = Card("example.ini")
pikachu = Card()
pikachu.write_config()
root = Tk()
root.geometry('1000x1000')
canvas = Canvas(root, width=999, height=999)
canvas.pack()

populate_card(pikachu)

pilImage = Image.open("card_from_python.jpg")
pilImage = pilImage.resize((732//3,1032//3), Image.ANTIALIAS)
image = ImageTk.PhotoImage(pilImage)
#imagesprite = canvas.create_image(500,200,image=image)
def spawnImage():
    canvas.create_image(500, 700, image=image)
def attack():
    pikachu.HP= int(pikachu.HP) - 30 #right now the info gets taken from .ini, needs to take from the object instead
    populate_card(pikachu)
    pilImage = Image.open("card_from_python.jpg")
    pilImage = pilImage.resize((732 // 3, 1032 // 3), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(pilImage)
    canvas.create_image(500, 700, image=image)
#root.after(1000, spawnImage(canvas, image))
btn = Button(root, text="Place card", command=spawnImage)
btn.place(x=500,y=970)
btn = Button(root, text="attack", command=attack)
btn.place(x=500,y=70)
root.mainloop()

