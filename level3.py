from entities import (Player, Tile, Grass, Coin, Enemy, Plant, cloud,
                     LuckyBlock, VerticalEnemy, Flag, HeartPowerUp,
                     TuboArriba, TuboAbajo, FirePowerUp,vidrio1,vidrio2,vidrio3,vidrio4,bloque,cornisa)

TILE = 48
LEVEL_MAP = [
    "                                                                                                                                                           ",
    "                                                                                                                                                           ",
    "                                                                                                                                                           ",
    "                                      M                                                                                                                    ",
    "                                            E                                                                                                              ",
    "                           MMME          GGGGG              MMMM                                                                                           ",
    "                          GGGGG          XXXXX              GGGG                E           MM   MM                                                       ",
    "                                         X12XX    M    GGG                   GGGG      M                     E                                             ",
    "                                         X43XX                               XXXX                        GGGGGG          MM                                ",
    "                            E       GGG  XXXXX                               X12X     GGG  V             XXXXXX                                            ",
    "                         GGGGGG     X1X  XX12X                         GG    X43X             GGG        XX12XX      GG    GG             XXXXXX           ",
    "                         XX12XX     X3X  XX43X              Q          XX    XXXX                        XX43XX      XX    XX             XX12XX           ",
    "                         XX43XX  M  XXX  XXXXX                         XX    X12X                  GG    XXXXXX      XX    XX             XX43XX        F  ",
    "  P                GG    XX12XX  G  X2X  X12XX                         XX    X43X                  XX    XX12XX  MMM XX    XX        E    XXXXXX        G  ",
    "GGGGGGGGGGGGGGGG   XX    XX43XX  X  X4X  X43XX     GGG     GGGG   GGG  XX    XXXX                  XX    XX43XX  GGG XX    XX    GGGGGGGGGXX12XXGGGGGGGGXGG",
    "XXXXXXXXXXXXXXXX   XX    XXXXXX  X  XXX  XXXXX     XXX     XXXX   XXX  XX    XXXX                  XX    XXXXXX  XXX XX    XX    XXXXXXXXXXX43XXXXXXXXXXXXX",
]

def load_level_3():
    hearts = []
    fire_powers = []  
    solids = []
    grasses = []
    coins = []
    enemies = []
    plants = []
    clouds = []
    flags = []
    player = None

    for j, row in enumerate(LEVEL_MAP):
        for i, ch in enumerate(row):
            x, y = i * TILE, j * TILE
            if ch == "X":
                solids.append(bloque((x, y)))
            elif ch == "G":
                grasses.append(cornisa((x, y)))
            elif ch == "P":
                player = Player((x, y), solids, coins, enemies, plants, clouds, grasses, flags, hearts, fire_powers)
            elif ch == "M":
                coins.append(Coin((x, y)))
            elif ch == "E":
                enemies.append(Enemy((x, y), solids, grasses, None))
            elif ch == "L":
                plants.append(Plant((x, y)))
            elif ch == "C":
                clouds.append(cloud((x, y)))
            elif ch == "B":
                grasses.append(LuckyBlock((x, y)))
            elif ch == "V":
                enemies.append(VerticalEnemy((x, y), y - 330, y + 100))
            elif ch == "F":
                flags.append(Flag((x, y)))
            elif ch == "H":
                hearts.append(HeartPowerUp((x, y)))
            elif ch == "Q":  
                fire_powers.append(FirePowerUp((x, y)))
            elif ch == "T":
                solids.append(TuboArriba((x, y)))
            elif ch == "t":
                solids.append(TuboAbajo((x, y)))
            elif ch == "1":
                solids.append(vidrio1((x, y)))
            elif ch == "2":
                solids.append(vidrio2((x, y)))
            elif ch == "3":
                solids.append(vidrio3((x, y)))
            elif ch == "4":
                solids.append(vidrio4((x, y)))

    for enemy in enemies:
        enemy.enemies_group = enemies

    return player, solids, coins, enemies, plants, clouds, grasses, flags, hearts, fire_powers
