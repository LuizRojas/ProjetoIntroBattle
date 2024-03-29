import pygame as pg
from game import *
from character import *
from random import randint

class Battle(SelectMenu):
    def __init__(self, game):
        SelectMenu.__init__(self, game)
        self.game = game
        self.running, self.playing = False, False
        self.bg_img = pg.transform.scale(pg.image.load('Background/cenario(lutas).png'), (1024, 768))
        self.ui_1 = pg.transform.scale(pg.image.load('UI/introcomp_menu(resized).png'), (650, 250))
        self.ui_2 = pg.transform.scale(self.ui_1, (360, 250))
        self.cursor = pg.transform.scale(pg.image.load('UI/introcomp_seta(resized).png'), (25, 25))
        self.turn = 'Player'
        self.coord = 'Defend'
        self.shift = Turn(self.game, self)
        self.coord_enemies = {'Witch': [850, 185, pg.transform.flip(SelectMenu(self.game).char.catalog['Witch'], True, False), Witch], 'Skeleton': [850, 350, pg.transform.flip(SelectMenu(self.game).char.catalog['Skeleton'], True, False), Skeleton]}
    
    def display_cursor(self, coord):
        self.positions = {'Attack': [45, 700], 'Defend': [260, 700], 'Witch': [850, 160], 'Skeleton': [850, 325]}
        
        self.imgx, self.imgy = self.positions[coord][0] + 50, self.positions[coord][1] - 50  # as coordenadas do cursor sao baseadas nas dos personagens
        img_rect = self.cursor.get_rect()
        img_rect.center = (self.imgx, self.imgy)  # coordenadas do cursor
        self.game.display.blit(pg.transform.rotate(self.cursor, 90), img_rect)
    
    def move_cursor(self):  # move o cursor de acordo com as acoes do usuario
        self.display_cursor(self.coord)
        if self.game.RIGHT_KEY:
            if self.coord == 'Attack':
                self.coord = 'Defend'
                    
        elif self.game.LEFT_KEY:
            if self.coord == 'Defend':
                self.coord = 'Attack'
    
    def check_input(self):  # verificando as acoes do jogador
        self.move_cursor()
        Turn.check_input(self)

    def show_hp(self):  # exibindo os pontos de vida de cada personagem
        self.health_points = [crew[0].show_hp(), crew[1].show_hp(), crew[2].show_hp()]  # pontos de vida iniciais dos personagens

        self.game.draw_text(f'{crew[0].__class__.__name__}  - {crew[0].show_hp()} / {self.health_points[0]}', 35, 850, 550, self.game.BLACK)
        self.game.draw_text(f'{crew[1].__class__.__name__} - {crew[1].show_hp()} / {self.health_points[1]}', 35, 850, 600, self.game.BLACK)
        self.game.draw_text(f'{crew[2].__class__.__name__} - {crew[2].show_hp()} / {self.health_points[2]}', 35, 850, 650, self.game.BLACK)

    def display_scenery(self):
        if self.running:
            self.check_input()
            
            self.game.check_events()

            self.game.display.fill(self.game.BLACK)
            self.game.display.blit(self.bg_img, (0, 0))
            self.game.display.blit(self.ui_1, (5, 510))
            self.game.display.blit(self.ui_2, (660, 510))

            # heroes
            if (crew[0].verifies_defeat()):
                crew[0].blit_character(50, 185, self.char.catalog[crew[0].__class__.__name__], self.game.display)

            if (crew[1].verifies_defeat()):
                crew[0].blit_character(90, 255, self.char.catalog[crew[1].__class__.__name__], self.game.display)

            if (crew[2].verifies_defeat()):
                crew[0].blit_character(50, 350, self.char.catalog[crew[2].__class__.__name__], self.game.display)

            if self.turn == 'Player':
                self.shift.hero_turn()

            # enemies
            Character().blit_character(self.coord_enemies['Witch'][0], self.coord_enemies['Witch'][1], self.coord_enemies['Witch'][2], self.game.display)
            Character().blit_character(self.coord_enemies['Skeleton'][0], self.coord_enemies['Skeleton'][1], self.coord_enemies['Skeleton'][2], self.game.display)

            self.game.main_menu.blit_screen()    
            self.game.reset_keys()

class Turn():
    def __init__(self, game, battle):
        self.game = game
        self.battle = battle
        self.enemy = 'Skeleton'
        self.choosing_enemy = False
        
    def hero_turn(self):
        self.count_turn = 0
        if self.battle.turn == 'Player':
            
            if self.count_turn == 0:
                self.crew_speed = [int(x.show_speed()) for x in crew]  # armazena a velocidade de cada integrante da equipe em uma lista
                self.max_speed = max(self.crew_speed)

                self.playing = ['', '']
                for count, speed in enumerate(self.crew_speed):
                    if speed == self.max_speed:
                        self.playing[0] = crew[count].__class__.__name__
                        self.playing[1] = count 

            self.game.draw_text(f"{self.playing[0]}'s turn!", 40, 175, 560, self.game.BLACK)
            self.game.draw_text('Attack', 35, 175, 650, self.game.BLACK)
            self.game.draw_text('Defend', 35, 390, 650, self.game.BLACK)
            self.battle.move_cursor()
            self.battle.show_hp()
        self.next_turn()

    def enemy_turn(self):
        '''if self.count_turn % 2 == 0:
            self.battle.coord['Witch'][3].attack_enemy(randint(0, len(crew) - 1))
        else:
            self.battle.coord['Skeleton'][3].attack_enemy(randint(0, len(crew) - 1))'''

    def next_turn(self):
        self.count_turn += 1
        self.enemy_turn()
    
    def select_enemy(self):
        self.choosing_enemy = True

        if self.choosing_enemy:
            self.fliped_cursor = pg.transform.scale(pg.image.load('UI/introcomp_seta(resized).png'), (25, 25))

            if self.coord == 'Attack':
                self.display_cursor(self.coord)
                if self.game.UP_KEY:
                    self.coord = 'Witch'
                
                elif self.game.DOWN_KEY:
                    self.coord = 'Skeleton'
                
            elif self.coord == 'Defend':  # caso o jogado selecione a opcao de defender, na proxima rodada o personagem estara defendendo
                crew[self.playing[1]].defend = True
                self.count_turn += 1

    def check_input(self):
        if self.coord == 'Attack':
            if self.game.z_KEY:
                if self.coord == 'Skeleton':
                    crew[self.playing[1]].attack_enemy(self.coord_enemies['Skeleton'][3])
                    self.next_turn()
                
                elif self.coord == 'Witch':
                    crew[self.playing[1]].attack_enemy(self.coord_enemies['Witch'][3])
                    self.next_turn()
        
        elif self.coord == 'Defend':
            if self.game.z_KEY:
                crew[self.playing[1]].defending = True
                self.next_turn()
