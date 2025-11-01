from entities import (Player, Tile, Grass, Coin, Enemy, Plant, cloud,
                     LuckyBlock, VerticalEnemy, Flag, HeartPowerUp,
                     TuboArriba, TuboAbajo, FirePowerUp)

TILE = 48
LEVEL_MAP = [
    "                                                                                                                                                                                                        ",
    "                                                                                                                                                                                                        ",
    "        C                     C                                   C        C                                 C                                      C                           C                       ",
    "                                                                                                                                                                                                        ",
    "   C                                               C                                       C           C                       C                                         C                          C   ",
    "            C                                C                        C              MM                           C       MMM                   C                                  C                    ",
    "                      B                                   C                     GGGGGGGG   GBG            B               GGG     GBBG                             C                       GG           ",
    "                                                                                                                                                                                          GXX   MM      ",
    "                                                                                                 MM                                              MM                                      GXXX           ",
    "                      H                      M                 B             Q                                                                                                          GXXXX           ",
    "                B   GBGBG                    T          T                   GBG            G    XB     B  B  B     G      MMM     GG                                   GGBG            GXXXXX           ",
    "                            T        T       t          t        MM                                                                     G  G         GG  G       MM                   GXXXXXX           ",
    "           V                t        t       t          t                V                         V                 V                 GX  XG       GXX  XG      XX                  GXXXXXXX      F    ",
    " P                   E      t  MM    t  E    t      E M t                     MM              E           MMM               E  E      GXX  XXG     GXXX  XXG     XX          E      GXXXXXXXX     GGG   ",
    "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG GGGGGGGGGGGGGGG   GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGXXX  XXXGGGGGXXXX  XXXGGGGGXXGGGGGGGGGGGGGGGGXXXXXXXXXXGGGGGXXXGGG",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX XXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XXXXXXXXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
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
