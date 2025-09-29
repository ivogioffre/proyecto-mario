# level2.py - CORRECCIÓN
# importamos todas las entidades
from entities import Player, Tile, Grass, Coin, Enemy, Plant, LuckyBlock, VerticalEnemy, Flag, cloud_level2, HeartPowerUp


# tamaño en pixeles de cada tile
TILE = 48  


# mapa del nivel 2
LEVEL_MAP_2 =[
    "                                                                                                                                                                                                         ",
    "                                                                                                                                                                                                         ",
    "        C                     C                                   C        C                                 C                                      C                           C                        ",
    "                                                                                                                                                                                                         ",
    "   C                                               C                                       C           C                       C                                         C                          C    ",
    "            C                                C                        C              MM                           C       MMM                   C                                  C                     ",
    "                      B                                   C                     GGGGGGGG   GBG             B              GGG     GBBG                             C                        GG           ",
    "                                                                                                                                                                                           GXX   MM      ",
    "                                                                                                 MM                                              MM                                       GXXX           ",
    "                                              MM                B                                                                                                                        GXXXX           ",
    "                B   GBGBG                     XX         XX                  GBG            G    XB     B  B  B     G      MMM     GG                                   GGBG            GXXXXX           ",
    "                            MM        XX      XX         XX       MM                                                                     G  G         GG  G       MM                   GXXXXXX           ",
    "           V                XX        XX      XX         XX               V                         V                 V                 GX  XG       GXX  XG      XX                  GXXXXXXX       F   ",
    " P          L        E      XX        XX E    XX     E   XX                    MM              E           MMM               E  E      GXX  XXG     GXXX  XXG     XX          E    XXGXXXXXXXX  LL L G L ",
    "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG  GGGGGGGGGGGGGGG   GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGXXX  XXXGGGGGXXXX  XXXGGGGGXXGGGGGGGGGGGGGGGXXXXXXXXXXXGGGGGGGXGGG",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XXXXXXXXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]


# función que devuelve los objetos del nivel 2
def load_level_2():
    solids = []
    grasses = []
    coins = []
    enemies = []
    plants = []
    clouds = []
    flags = []
    hearts = []
    player = None


    for j, row in enumerate(LEVEL_MAP_2):
        for i, ch in enumerate(row):
            x, y = i * TILE, j * TILE
            if ch == "X":
                solids.append(Tile((x, y)))
            elif ch == "G":
                grasses.append(Grass((x, y)))
            elif ch == "P":
                # CORREGIDO: eliminar el parámetro "powerups" que no existe
                player = Player((x, y), solids, coins, enemies, plants, clouds, grasses, flags)
            elif ch == "M":
                coins.append(Coin((x, y)))
            elif ch == "E":
                enemies.append(Enemy((x, y), solids, grasses, None))
            elif ch == "L":
                plants.append(Plant((x, y)))
            elif ch == "C":
                clouds.append(cloud_level2((x, y)))
            elif ch == "B":
                grasses.append(LuckyBlock((x, y)))
            elif ch == "V":
                # CORREGIDO: velocidad aumentada de 2 a 3 para igualar al enemigo horizontal
                enemies.append(VerticalEnemy((x, y), y - 330, y + 100, speed=3))
            elif ch == "F":
                flags.append(Flag((x, y)))
            elif ch == "H":
                hearts.append(HeartPowerUp((x, y)))


    # para que los enemigos choquen entre sí
    for enemy in enemies:
        enemy.enemies_group = enemies


    return player, solids, coins, enemies, plants, clouds, grasses, flags, hearts