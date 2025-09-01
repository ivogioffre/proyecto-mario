from entities import Player, Tile, Grass, Coin, Enemy, Plant, cloud, LuckyBlock, VerticalEnemy

TILE = 48
LEVEL_MAP = [
    "                                                                                                                                                                                                         ",
    "                                                                                                                                                                                                         ",
    "                                                                                                                                                                                                         ",
    "                                                                                                                                                                                                         ",
    "                                                  C                                       C           C                       C                                         C                          C     ",
    "            C                                C                        C           E  MM                           C       MMM                   C                                  C                     ",
    "                      B                                   C                     GGGGGGGG   GBG             B              GGG     GBBG                             C                        GG           ",
    "                                                                                                                                                                                           GXX   MM      ",
    "                                                                                                 MM                                              MM                                       GXXX       F   ",
    "                                              MM                B                                                                                                                        GXXXX       F   ",
    "                B   GBGBG                     XX         XX                  GBG            G    XB     B  B  B     G      MMM     GG                                   GGBG            GXXXXX       F   ",
    "                            MM        XX      XX         XX       MM                                                                     G  G         GG  G       MM                   GXXXXXX       F   ",
    "           V                XX        XX      XX         XX               V                         V                 V                 GX  XG       GXX  XG      XX                  GXXXXXXX       F   ",
    " P                   E      XX        XX E    XX     E   XX                    MM              E           MMM               E  E      GXX  XXG     GXXX  XXG     XX          E    XXGXXXXXXXX  LL L G L ",
    "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG  GGGGGGGGGGGGGGG   GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGXXX  XXXGGGGGXXXX  XXXGGGGGXXGGGGGGGGGGGGGGGXXXXXXXXXXXGGGGGGGXGGG",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XXXXXXXXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

def load_level():
    solids = []
    grasses = []
    coins = []
    enemies = []
    plants = []
    clouds = []
    player = None

    for j, row in enumerate(LEVEL_MAP):
        for i, ch in enumerate(row):
            x, y = i * TILE, j * TILE
            if ch == "X":
                solids.append(Tile((x, y)))
            elif ch == "G":
                grasses.append(Grass((x, y)))
            elif ch == "P":
                player = Player((x, y), solids, coins, enemies, plants, clouds, grasses)
            elif ch == "M":
                coins.append(Coin((x, y)))
            elif ch == "E":
                enemies.append(Enemy((x, y), solids, grasses, None))  # <-- Pasa None por ahora
            elif ch == "L":
                plants.append(Plant((x, y)))
            elif ch == "C":
                clouds.append(cloud((x, y)))
            elif ch == "B":
                grasses.append(LuckyBlock((x, y)))
            elif ch == "V":
                enemies.append(VerticalEnemy((x, y), y - 330, y + 100))

    # Asignar la lista completa de enemigos a cada enemigo para colisiones
    for enemy in enemies:
        enemy.enemies_group = enemies

    return player, solids, coins, enemies, plants, clouds, grasses