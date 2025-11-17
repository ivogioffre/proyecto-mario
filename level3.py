from entities import (Player, Tile, Grass, Coin, Enemy, Plant, cloud,
                     LuckyBlock, VerticalEnemy, Flag, HeartPowerUp,
                     TuboArriba, TuboAbajo, FirePowerUp)

TILE = 48
LEVEL_MAP = [
    "                                                                                                                                                           ",
    "                                                                                                                                                           ",
    "                                                                                                                                                           ",
    "                                     MM                                                                                                                    ",
    "                                              E                                                                                                            ",
    "                           MMME         GGGGGGG             MMMM                                                                                           ",
    "                          GGGGG          XXXXX              GGGG                E           MM   MM                                           GG           ",
    "                                         XXXXX    M    GGG                  GGGGGG     M                     E                                XX           ",
    "                                         XXXXX                               XXXX                       GGGGGGGG         MM                 GGXX           ",
    "                                   GGGGG XXXXX                               XXXX     GGG                XXXXXX                             XXXX           ",
    "                        GGGGGGGG    XXX  XXXXX                        GGG    XXXX             GGG        XXXXXX     GGGG  GGGG            GGXXXX           ",
    "                         XXXXXX     XXX  XXXXX             Q           X     XXXX                        XXXXXX      XX    XX             XXXXXX           ",
    "                         XXXXXX  M  XXX  XXXXX                         X     XXXX                 GGGG   XXXXXX      XX    XX             XXXXXX        F  ",
    "  P               GGGG   XXXXXX GGG XXX  XXXXX                         X     XXXX                  XX    XXXXXX  MMM XX    XX        E    XXXXXX        G  ",
    "GGGGGGGGGGGGGGGG   XX    XXXXXX  X  XXX  XXXXX    GGGG     GGGGG GGGGG X     XXXX                  XX    XXXXXX  GGG XX    XX    GGGGGGGGGXXXXXXGGGGGGGGXGG",
    "XXXXXXXXXXXXXXXX   XX    XXXXXX  X  XXX  XXXXX     XX       XXX   XXX  X     XXXX                  XX    XXXXXX   X  XX    XX    XXXXXXXXXXXXXXXXXXXXXXXXXX",
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
                solids.append(Tile((x, y)))
            elif ch == "G":
                grasses.append(Grass((x, y)))
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

    for enemy in enemies:
        enemy.enemies_group = enemies

    return player, solids, coins, enemies, plants, clouds, grasses, flags, hearts, fire_powers
