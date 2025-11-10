from entities import Player, TileLevel2, GrassLevel2, Coin, Enemy, Plant, LuckyBlock, VerticalEnemy, Flag, cloud_level2, HeartPowerUp ,TuboArriba, TuboAbajo, FirePowerUp



# tamaño en pixeles de cada tile
TILE = 48  




# mapa del nivel 2
LEVEL_MAP_2 =[
    "",
    "",
    "",
    "",
    "                                                    GGGG  GGGGGG  GGGG                                                                                                  ",
    "                                                    XXXX  XXXXXX  XXXX              MMMMMM                                                                              ",
    "                                                    XX        XX   X    GG                                                                                              ",
    "                                         G          XX        XX   X    XX                                                                   M             GGG          ",
    "                                       G X  G G     XX        XX   X    XX          GGGGGG                                                  GGG                         ",
    "                             V         X X QX X     XX H    MMXX   XM   XX    E     XXXXXX                                 M                       E                    ",
    "                       GGG M           XGX  XGX     XXGG  GGGGXX   XXX  XX  GGGGGG                            T           GG            GG       GGGGGG               F ",
    "                     G XXX G   G                      BX     B                                          T     t     T     XX           GXX                      GGGGGGGG",
    "                   G X XXX X   X G                                                                      t     t     t     XX          GXXX                      XXXXXXXX",
    " P               G X X XXX X E X X                         E  E E                             E    M    t   E t  E  t     XX         GXXXX            MM        XXXXXXXX",
    "GGGGGGGGGGGGGGGGGX X X XXX XGGGXGXGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG   GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG  XX  GGGGGGGXXXXX  GGG  GGGGGGGG  GGG  XXXXXXXX",
    "XXXXXXXXXXXXXXXXXX X X XXX XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XX  XXXXXXXXXXXX       XXXXXXXX       XXXXXXXX",
]




# función que devuelve los objetos del nivel 2
def load_level_2():
    solids = []
    fire_powers = []
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
                solids.append(TileLevel2((x, y)))
            elif ch == "G":
                grasses.append(GrassLevel2((x, y)))
            elif ch == "P":
                player = Player((x, y), solids, coins, enemies, plants, clouds, grasses, flags, hearts, fire_powers)
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
                # velocidad aumentada de 2 a 3 para igualar al enemigo horizontal
                enemies.append(VerticalEnemy((x, y), y - 330, y + 100, speed=3))
            elif ch == "F":
                flags.append(Flag((x, y)))
            elif ch == "H":
                hearts.append(HeartPowerUp((x, y)))
            elif ch == "T":
                solids.append(TuboArriba((x, y)))
            elif ch == "t":
                solids.append(TuboAbajo((x, y)))
            elif ch == "Q":  
                fire_powers.append(FirePowerUp((x, y)))


    # para que los enemigos choquen entre sí
    for enemy in enemies:
        enemy.enemies_group = enemies


    return player, solids, coins, enemies, plants, clouds, grasses, flags, hearts, fire_powers