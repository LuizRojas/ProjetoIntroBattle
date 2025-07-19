import pygame as pg
from pygame.locals import *
import os
from random import randint

# --- Classes de Personagens ---
class Character():
    def __init__(self):
        self.defending = False
        self.health = 0
        self.max_health = 0 
        self.attack = 0
        self.defense = 0
        self.speed = 0
        self.defeat = False 
        
        current_dir = os.path.dirname(__file__)
        ui_bg_path = os.path.join(current_dir, 'UI', 'introcomp_menu(resized).png')
        
        self.ui_bg = pg.transform.scale(pg.image.load(ui_bg_path), (150, 150))
        
        self.catalog = {
            'Wizard': pg.transform.flip(pg.transform.scale(pg.image.load(os.path.join(current_dir, 'Personagens', 'mago(final).png')), (90, 90)), True, False),
            'Witch': pg.transform.scale(pg.image.load(os.path.join(current_dir, 'Personagens', 'bruxa.png')), (90, 90)),
            'Rogue': pg.transform.scale(pg.image.load(os.path.join(current_dir, 'Personagens', 'vampiro.png')), (90, 90)),
            'Skeleton': pg.transform.scale(pg.image.load(os.path.join(current_dir, 'Personagens', 'caveira.png')), (90, 90)),
            'Priest': pg.transform.scale(pg.image.load(os.path.join(current_dir, 'Personagens', 'clerigo(sem_sombra).png')), (90, 90)),
            'Paladin': pg.transform.scale(pg.image.load(os.path.join(current_dir, 'Personagens', 'paladino.png')), (90, 90)),
            'Hunter': pg.transform.scale(pg.image.load(os.path.join(current_dir, 'Personagens', 'cacadora.png')), (90, 90)),
        }

    def take_damage(self, damage):
        if self.defending:
            damage = max(0, damage - (self.defense * 0.5))
        else:
            damage = max(0, damage - self.defense)
        self.health = max(0, self.health - damage)
        if self.health == 0:
            self.defeat = True

    def attack_target(self, target):
        damage = self.attack * 2
        target.take_damage(damage)

    def set_defending(self, status):
        self.defending = status

    def verifies_defeat(self):
        return self.health <= 0
    
    def blit_character(self, x, y, img, screen):
        screen.blit(img, (x, y))
    
    def show_hp(self):
        return self.health
    
    def show_attack(self):
        return self.attack
    
    def show_defense(self):
        return self.defense

    def show_speed(self):
        return self.speed

class Wizard(Character):
    def __init__(self):
        super().__init__()
        self.health = 80
        self.max_health = 80 
        self.attack = 8
        self.defense = 5
        self.speed = 1
        self.img = self.catalog['Wizard']

class Witch(Character):
    def __init__(self):
        super().__init__()
        self.health = 75
        self.max_health = 75 
        self.attack = 9
        self.defense = 4
        self.speed = 3
        self.img = self.catalog['Witch']

class Rogue(Character):
    def __init__(self):
        super().__init__()
        self.health = 85
        self.max_health = 85 
        self.attack = 10
        self.defense = 2
        self.speed = 5
        self.img = self.catalog['Rogue']

class Skeleton(Character):
    def __init__(self):
        super().__init__()
        self.health = 70
        self.max_health = 70 
        self.attack = 11
        self.defense = 6
        self.speed = 4
        self.img = self.catalog['Skeleton']

class Priest(Character):
    def __init__(self):
        super().__init__()
        self.health = 80    
        self.max_health = 80 
        self.attack = 7
        self.defense = 8
        self.speed = 4
        self.img = self.catalog['Priest']

class Paladin(Character):
    def __init__(self):
        super().__init__()
        self.health = 90
        self.max_health = 90 
        self.attack = 5
        self.defense = 6
        self.speed = 1
        self.img = self.catalog['Paladin']

class Hunter(Character):
    def __init__(self):
        super().__init__()
        self.health = 85
        self.max_health = 85 
        self.attack = 6
        self.defense = 3
        self.speed = 5
        self.img = self.catalog['Hunter']

# --- Classes de Menu ---
class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W // 2, self.game.DISPLAY_H // 2
        self.run_display = True
        
        current_dir = os.path.dirname(__file__)
        cursor_img_path = os.path.join(current_dir, 'UI', 'introcomp_seta(resized).png')

        self.cursor_img = pg.transform.scale(pg.image.load(cursor_img_path), (18, 18))
        self.cursor_rect = pg.Rect(0, 0, 40, 40)
        self.offset = - 100
    
    def draw_cursor(self):
        self.game.draw_text('>', 25, self.cursor_rect.x, self.cursor_rect.y, self.game.WHITE)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pg.display.flip()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.state = 'Start'
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 60
        self.exitx, self.exity = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Main Menu', 35, self.game.DISPLAY_W // 2, self.game.DISPLAY_H // 2 - 20, self.game.WHITE)
            self.game.draw_text('Start', 35, self.startx, self.starty, self.game.WHITE)
            self.game.draw_text('Credits', 35, self.creditsx, self.creditsy, self.game.WHITE)
            self.game.draw_text('Exit', 35, self.exitx, self.exity, self.game.WHITE)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'

        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Exit'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
    
    def check_input(self):
        self.move_cursor()
        if self.game.z_KEY:
            if self.state == 'Start':
                self.game.playing = True
                self.game.current_menu = self.game.selection_menu
                self.game.selection_menu.running = True
                self.game.play_music('inspiration') # Toca música de seleção de personagem
            
            elif self.state == 'Credits':
                self.game.current_menu = self.game.credits
                self.game.credits.run_display = True

            elif self.state == 'Exit':
                self.game.running, self.game.playing = False, False

            self.run_display = False

class SelectMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.position = 'Priest'
        
        current_dir = os.path.dirname(__file__)
        bg_path = os.path.join(current_dir, 'Background', 'cenario(menu).png')
        self.bg = pg.transform.scale(pg.image.load(bg_path), (1024, 768))
        self.running = False
        self.char = Character()
        self.state = {
            'Priest': [245, 130], 'Paladin': [465, 130], 'Hunter': [685, 130],
            'Wizard': [335, 475], 'Rogue': [565, 475],
        }
        self.available_characters = {
            'Priest': Priest(),
            'Paladin': Paladin(),
            'Hunter': Hunter(),
            'Wizard': Wizard(),
            'Rogue': Rogue()
        }
    
    def draw_cursor(self, position):
        self.imgx, self.imgy = self.state[position][0] + 50, self.state[position][1] - 50
        current_dir = os.path.dirname(__file__)
        cursor_img_select_path = os.path.join(current_dir, 'UI', 'introcomp_seta(resized).png')
        self.curr_img = pg.transform.scale(pg.image.load(cursor_img_select_path), (35, 35))
        img_rect = self.curr_img.get_rect()
        img_rect.center = (self.imgx, self.imgy)
        self.game.display.blit(self.curr_img, img_rect)
    
    def move_cursor(self):
        if self.game.RIGHT_KEY:
            if self.position == 'Priest':
                self.position = 'Paladin'
            elif self.position == 'Paladin':
                self.position = 'Hunter'
            elif self.position == 'Hunter':
                self.position = 'Wizard'
            elif self.position == 'Wizard':
                self.position = 'Rogue'
            elif self.position == 'Rogue':
                self.position = 'Priest'

        elif self.game.LEFT_KEY:
            if self.position == 'Priest':
                self.position = 'Rogue'
            elif self.position == 'Rogue':
                self.position = 'Wizard'
            elif self.position == 'Wizard':
                self.position = 'Hunter'
            elif self.position == 'Hunter':
                self.position = 'Paladin'
            elif self.position == 'Paladin':
                self.position = 'Priest'

        elif self.game.UP_KEY:
            if self.position == 'Wizard':
                self.position = 'Paladin'
            elif self.position == 'Rogue':
                self.position = 'Hunter'

        elif self.game.DOWN_KEY:
            if self.position == 'Priest':
                self.position = 'Wizard'
            elif self.position == 'Paladin':
                self.position = 'Rogue'
            elif self.position == 'Hunter':
                self.position = 'Wizard'
        
        self.draw_cursor(self.position)

    def display_menu(self):
        if self.running:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)

            self.game.display.blit(self.bg, (0,0))
            self.game.draw_text('Select your characters', 50, self.game.DISPLAY_W // 2, self.game.DISPLAY_H // 2 - 20, self.game.WHITE)
            self.game.draw_text(f'Characters selected: {len(self.game.crew)}/3', 30, self.game.DISPLAY_W // 2, 50, self.game.WHITE)

            self.game.display.blit(self.char.ui_bg, (210, 105))
            self.game.display.blit(self.char.ui_bg, (430, 105))
            self.game.display.blit(self.char.ui_bg, (650, 105))
            self.game.display.blit(self.char.ui_bg, (310, 450))
            self.game.display.blit(self.char.ui_bg, (535, 450))

            self.char.blit_character(self.state['Priest'][0], self.state['Priest'][1], self.char.catalog['Priest'], self.game.display)
            self.char.blit_character(self.state['Paladin'][0], self.state['Paladin'][1], self.char.catalog['Paladin'], self.game.display)
            self.char.blit_character(self.state['Hunter'][0], self.state['Hunter'][1], self.char.catalog['Hunter'], self.game.display)
            self.char.blit_character(self.state['Wizard'][0], self.state['Wizard'][1], self.char.catalog['Wizard'], self.game.display)
            self.char.blit_character(self.state['Rogue'][0], self.state['Rogue'][1], self.char.catalog['Rogue'], self.game.display)

            self.game.draw_text('Priest', 20, 275, 230, self.game.BLACK)
            self.game.draw_text('Paladin', 20, 510, 230, self.game.BLACK)
            self.game.draw_text('Hunter', 20, 725, 230, self.game.BLACK)
            self.game.draw_text('Wizard', 20, 385, 575, self.game.BLACK)
            self.game.draw_text('Rogue', 20, 605, 575, self.game.BLACK)

            self.draw_cursor(self.position)
            self.game.reset_keys()
            self.blit_screen()

    def check_input(self):
        self.move_cursor()
        if self.game.z_KEY:
            selected_char_instance = self.available_characters[self.position]
            self.select_team(selected_char_instance)
        
        elif self.game.x_KEY:
            self.running = False
            self.game.playing = False
            self.game.current_menu = self.game.main_menu
            self.game.crew = []
            self.game.play_music('main_menu') # Retorna à música do menu principal

        if len(self.game.crew) == 3:
            self.running = False
            self.game.battle_system = Battle(self.game, self.game.crew)
            self.game.current_menu = self.game.battle_system
            self.game.battle_system.running = True
            # A música da batalha será definida dentro do Battle, se houver

    def select_team(self, character_instance):
        if len(self.game.crew) < 3:
            if not any(isinstance(char, type(character_instance)) for char in self.game.crew):
                self.game.crew.append(character_instance)
                print(f"Adicionado {character_instance.__class__.__name__} à equipe. Equipe: {[c.__class__.__name__ for c in self.game.crew]}")
            else:
                print(f"{character_instance.__class__.__name__} já está na equipe.")
        else:
            print("Equipe já está completa!")

class CreditsMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.x, self.y = self.game.DISPLAY_W // 2, 10
        self.credits = ['--- Creditos ---',
                        '',
                        'Artes:',
                        'Augusto Moraes Alves',
                        'Bernardo Seibert',
                        'Geisson Venancio do Nascimento',
                        'Giulia Guimaraes',
                        'Kaique Taylor Gripa dos Santos',
                        'Kiara Pezzin Silva',
                        'Raquel Paulo Silva',
                        'Rhuan dos Santos',
                        '',
                        'Desenvolvimento do jogo:',
                        'Luiz Rojas',
                        'Octavio Sales',
                        'Karla Sancio',
                        'Joao Gabriel de Barros Rocha',
                        '',
                        'Documentacao:',
                        'Victor Aguiar Marques']

    def display_menu(self):
        self.run_display = True

        self.y_offset = 65
        self.lines = []
        for line in self.credits:
            self.lines.append((line, self.y_offset))
            self.y_offset += 25

        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            
            for content in self.lines:
                self.game.draw_text(content[0], 35, self.x, content[1], self.game.WHITE)

            self.game.reset_keys()
            self.blit_screen()

    def check_input(self):
        self.game.check_events()
        if self.game.x_KEY:
            self.run_display = False
            self.game.current_menu = self.game.main_menu # Volta para o menu principal

class GameOverMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.outcome = "" # "Victory" or "Defeat"

    def set_outcome(self, outcome):
        self.outcome = outcome
        if outcome == "Vitória!":
            self.game.play_music('victory')
        elif outcome == "Derrota!":
            self.game.play_music('defeat')

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            
            self.game.draw_text('Game Over', 50, self.mid_w, self.mid_h - 50, self.game.WHITE)
            self.game.draw_text(self.outcome, 40, self.mid_w, self.mid_h + 20, self.game.WHITE)
            self.game.draw_text('Pressione Z para voltar ao Menu Principal', 25, self.mid_w, self.mid_h + 100, self.game.WHITE)
            
            self.blit_screen()

    def check_input(self):
        if self.game.z_KEY:
            self.run_display = False
            self.game.current_menu = self.game.main_menu # Volta para o menu principal
            self.game.playing = False # Sai do estado de "jogando"
            self.game.play_music('main_menu') # Retorna à música do menu principal

# --- Classes do Sistema de Batalha ---
class Turn():
    def __init__(self, game, battle):
        self.game = game
        self.battle = battle
        self.turn_count = 0
        
    def hero_turn(self):
        pass

    def enemy_turn(self):
        enemy_acting = self.battle.current_character_acting
        
        if enemy_acting and not enemy_acting.verifies_defeat():
            living_heroes = [hero for hero in self.battle.crew if not hero.verifies_defeat()]
            if living_heroes:
                target_hero = living_heroes[randint(0, len(living_heroes) - 1)]
                enemy_acting.attack_target(target_hero)
                print(f"{enemy_acting.__class__.__name__} atacou {target_hero.__class__.__name__}")
            else:
                print("Não há heróis vivos para o inimigo atacar.")

    def next_turn(self):
        for hero in self.battle.crew:
            hero.set_defending(False)

        self.battle.current_turn_index = (self.battle.current_turn_index + 1) % len(self.battle.turn_order)
        self.battle.current_character_acting = self.battle.turn_order[self.battle.current_turn_index]

        while self.battle.current_character_acting.verifies_defeat():
            self.battle.current_turn_index = (self.battle.current_turn_index + 1) % len(self.battle.turn_order)
            self.battle.current_character_acting = self.battle.turn_order[self.battle.current_turn_index]
        
        self.battle.action_selected = False
        self.battle.choosing_target = False
        print(f"Agora é o turno de: {self.battle.current_character_acting.__class__.__name__}")

class Battle(SelectMenu): 
    def __init__(self, game, crew):
        super().__init__(game)
        self.game = game
        self.crew = crew
        self.running = False # A batalha não começa imediatamente, o SelectMenu a inicia
        self.playing = True 
        
        current_dir = os.path.dirname(__file__)
        bg_img_path = os.path.join(current_dir, 'Background', 'cenario(lutas).png')
        ui_1_path = os.path.join(current_dir, 'UI', 'introcomp_menu(resized).png')
        cursor_path = os.path.join(current_dir, 'UI', 'introcomp_seta(resized).png')

        self.bg_img = pg.transform.scale(pg.image.load(bg_img_path), (1024, 768))
        self.ui_1 = pg.transform.scale(pg.image.load(ui_1_path), (650, 250))
        self.ui_2 = pg.transform.scale(self.ui_1, (360, 250))
        self.cursor = pg.transform.scale(pg.image.load(cursor_path), (25, 25))
        
        self.turn_order = []
        self.current_turn_index = 0
        self.current_character_acting = None

        self.enemy_witch = Witch()
        self.enemy_skeleton = Skeleton()
        self.enemies = [self.enemy_witch, self.enemy_skeleton]

        self.coord = 'Attack'
        self.target_coord = 'Witch'

        self.action_selected = False
        self.choosing_target = False
        
        self.shift = Turn(self.game, self)

        self.coord_heroes = {
            self.crew[0].__class__.__name__: [50, 185],
            self.crew[1].__class__.__name__: [90, 255],
            self.crew[2].__class__.__name__: [50, 350],
        }

        self.coord_enemies = {
            'Witch': [850, 185, pg.transform.flip(self.char.catalog['Witch'], True, False), self.enemy_witch],
            'Skeleton': [850, 350, pg.transform.flip(self.char.catalog['Skeleton'], True, False), self.enemy_skeleton]
        }
        self.initialize_turn_order()
        # Música da batalha
        # self.game.play_music('battle') # Descomente se tiver uma música específica para a batalha

    def initialize_turn_order(self):
        all_characters = self.crew + self.enemies
        self.turn_order = sorted(all_characters, key=lambda char: char.show_speed(), reverse=True)
        self.current_turn_index = 0
        self.current_character_acting = self.turn_order[self.current_turn_index]
        print(f"Ordem de turnos: {[char.__class__.__name__ for char in self.turn_order]}")


    def display_cursor(self, coord_type, position_key):
        action_positions = {'Attack': [45, 700], 'Defend': [260, 700]}
        target_positions = {'Witch': [self.coord_enemies['Witch'][0] - 80, self.coord_enemies['Witch'][1] + 20], 
                            'Skeleton': [self.coord_enemies['Skeleton'][0] - 80, self.coord_enemies['Skeleton'][1] + 20]}

        if coord_type == 'action':
            positions = action_positions
        elif coord_type == 'target':
            positions = target_positions
        else:
            return

        self.imgx, self.imgy = positions[position_key][0] + 50, positions[position_key][1] - 50
        img_rect = self.cursor.get_rect()
        img_rect.center = (self.imgx, self.imgy)
        self.game.display.blit(pg.transform.rotate(self.cursor, 90), img_rect)
    
    def move_action_cursor(self):
        if self.game.RIGHT_KEY:
            if self.coord == 'Attack':
                self.coord = 'Defend'
        elif self.game.LEFT_KEY:
            if self.coord == 'Defend':
                self.coord = 'Attack'
        self.display_cursor('action', self.coord)

    def move_target_cursor(self):
        living_enemies_keys = [key for key, (x, y, img, instance) in self.coord_enemies.items() if not instance.verifies_defeat()]
        if not living_enemies_keys:
            return

        current_index = living_enemies_keys.index(self.target_coord)
        if self.game.UP_KEY:
            current_index = (current_index - 1) % len(living_enemies_keys)
        elif self.game.DOWN_KEY:
            current_index = (current_index + 1) % len(living_enemies_keys)
        
        self.target_coord = living_enemies_keys[current_index]
        self.display_cursor('target', self.target_coord)

    def check_input(self):
        current_char = self.current_character_acting

        if current_char in self.crew:
            if not self.action_selected:
                self.move_action_cursor()
                if self.game.z_KEY:
                    if self.coord == 'Attack':
                        self.action_selected = True
                        self.choosing_target = True
                        current_char.set_defending(False)
                        living_enemies_keys = [key for key, (x, y, img, instance) in self.coord_enemies.items() if not instance.verifies_defeat()]
                        if living_enemies_keys:
                            self.target_coord = living_enemies_keys[0]

                    elif self.coord == 'Defend':
                        current_char.set_defending(True)
                        self.shift.next_turn()
                        self.action_selected = False
                        self.choosing_target = False
            elif self.choosing_target:
                self.move_target_cursor()
                if self.game.z_KEY:
                    target_enemy_instance = self.coord_enemies[self.target_coord][3]
                    current_char.attack_target(target_enemy_instance)
                    self.shift.next_turn()
                    self.action_selected = False
                    self.choosing_target = False
        
    def show_hp(self):
        for i, hero in enumerate(self.crew):
            self.game.draw_text(f'{hero.__class__.__name__} - {hero.show_hp()} / {hero.max_health}', 35, 850, 550 + (i * 50), self.game.BLACK)
        
        for enemy_name, (x, y, img, enemy_instance) in self.coord_enemies.items():
            if not enemy_instance.verifies_defeat():
                text_x = x + 30
                text_y = y - 20
                self.game.draw_text(enemy_name, 25, text_x, text_y, self.game.WHITE)
                self.game.draw_text(f'HP: {enemy_instance.show_hp()} / {enemy_instance.max_health}', 20, text_x, text_y + 25, self.game.WHITE)


    def display_scenery(self):
        if self.running:
            self.game.check_events()
            self.game.display.fill(self.game.BLACK)
            self.game.display.blit(self.bg_img, (0, 0))
            self.game.display.blit(self.ui_1, (5, 510))
            self.game.display.blit(self.ui_2, (660, 510))

            for hero in self.crew:
                if not hero.verifies_defeat():
                    x, y = self.coord_heroes[hero.__class__.__name__]
                    hero.blit_character(x, y, hero.img, self.game.display)

            for enemy_name, (x, y, img, enemy_instance) in self.coord_enemies.items():
                if not enemy_instance.verifies_defeat():
                    enemy_instance.blit_character(x, y, img, self.game.display)

            if self.current_character_acting:
                if self.current_character_acting in self.crew:
                    self.game.draw_text(f"{self.current_character_acting.__class__.__name__}'s turn!", 40, 175, 560, self.game.BLACK)
                    self.game.draw_text('Attack', 35, 175, 650, self.game.BLACK)
                    self.game.draw_text('Defend', 35, 390, 650, self.game.BLACK)
                    
                    if not self.action_selected:
                        self.display_cursor('action', self.coord)
                    elif self.choosing_target:
                        self.display_cursor('target', self.target_coord)

                    self.check_input()

                else:
                    self.shift.enemy_turn()
                    self.shift.next_turn()

            self.show_hp()
            self.blit_screen()
            self.game.reset_keys()

            self.check_game_over()

    def check_game_over(self):
        all_heroes_defeated = all(hero.verifies_defeat() for hero in self.crew)
        all_enemies_defeated = all(enemy.verifies_defeat() for enemy in self.enemies)

        if all_heroes_defeated:
            self.running = False
            self.game.current_menu = self.game.game_over_menu
            self.game.game_over_menu.set_outcome("Derrota!")
            self.game.game_over_menu.run_display = True
            self.game.crew = []
            # Reinicializa inimigos para a próxima batalha
            self.enemy_witch = Witch()
            self.enemy_skeleton = Skeleton()
            self.enemies = [self.enemy_witch, self.enemy_skeleton]

        elif all_enemies_defeated:
            self.running = False
            self.game.current_menu = self.game.game_over_menu
            self.game.game_over_menu.set_outcome("Vitória!")
            self.game.game_over_menu.run_display = True
            self.game.crew = []
            # Reinicializa inimigos para a próxima batalha
            self.enemy_witch = Witch()
            self.enemy_skeleton = Skeleton()
            self.enemies = [self.enemy_witch, self.enemy_skeleton]

# --- Classe Game Principal ---
class Game():
    def __init__(self):
        pg.init()
        pg.mixer.init() # Inicializa o mixer de áudio
        
        self.running = True
        self.playing = False 
        self.crew = []

        self.z_KEY, self.x_KEY, self.RIGHT_KEY, self.LEFT_KEY, self.UP_KEY, self.DOWN_KEY = False, False, False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 1024, 768
        self.display = pg.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pg.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))

        pg.display.set_caption('Intro Battle')
        current_dir = os.path.dirname(__file__)
        font_path = os.path.join(current_dir, 'Programa', 'FreePixel.ttf')
        self.font_name = font_path

        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)

        # Músicas
        self.music_paths = {
            'main_menu': os.path.join(current_dir, 'Musicas', 'BoxCat Games - Inspiration.mp3'), # Música para o menu principal
            'inspiration': os.path.join(current_dir, 'Musicas', 'BoxCat Games - Inspiration.mp3'), # Música para seleção de personagens
            'defeat': os.path.join(current_dir, 'Musicas', 'BoxCat Games - Defeat.mp3'),
            'victory': os.path.join(current_dir, 'Musicas', 'BoxCat Games - Victory.mp3'),
            # 'battle': os.path.join(current_dir, 'musicas', 'SUAMUSICAAQUI.mp3'), # Exemplo de música de batalha
        }
        self.current_music = None # Rastreia qual música está tocando

        self.main_menu = MainMenu(self)
        self.credits = CreditsMenu(self)
        self.selection_menu = SelectMenu(self)
        self.game_over_menu = GameOverMenu(self)
        self.current_menu = self.main_menu # Inicia no menu principal

        self.battle_system = None 

        self.play_music('main_menu') # Toca a música do menu principal ao iniciar

    def play_music(self, track_name):
        new_music_path = self.music_paths.get(track_name)
        if new_music_path and (self.current_music != track_name or not pg.mixer.music.get_busy()):
            pg.mixer.music.load(new_music_path)
            pg.mixer.music.play(-1) # Loop infinito
            self.current_music = track_name

    def game_loop(self):
        clock = pg.time.Clock()
        while self.running:
            self.check_events()

            if self.playing:
                self.display.fill(self.BLACK)

                if self.selection_menu.running:
                    self.selection_menu.display_menu()
                elif self.battle_system and self.battle_system.running:
                    self.battle_system.display_scenery()
                elif self.game_over_menu.run_display:
                    self.game_over_menu.display_menu()
            else:
                self.current_menu.display_menu()

            self.window.blit(self.display, (0, 0))
            pg.display.flip()
            self.reset_keys()
            clock.tick(60)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                self.playing = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    self.z_KEY = True
                if event.key == pg.K_x:
                    self.x_KEY = True
                if event.key == pg.K_RIGHT:
                    self.RIGHT_KEY = True
                if event.key == pg.K_LEFT:
                    self.LEFT_KEY = True
                if event.key == pg.K_UP:
                    self.UP_KEY = True
                if event.key == pg.K_DOWN:
                    self.DOWN_KEY = True

    def reset_keys(self):
        self.z_KEY, self.x_KEY, self.RIGHT_KEY, self.LEFT_KEY, self.UP_KEY, self.DOWN_KEY = False, False, False, False, False, False

    def draw_text(self, text, size, x, y, color):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

# --- Instância do Jogo e Loop Principal ---
if __name__ == '__main__':
    g = Game()
    g.game_loop()
    pg.quit() # Garante que o Pygame seja encerrado corretamente