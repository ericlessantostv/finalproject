import asyncio
import json
import random
from socket import socket

import arcade
import pathlib
from math import dist
from pathlib import Path

import Server
from PlayerLocation import *
#Eric Santos

FRAME_HEIGHT = 63
FRAME_WIDTH = 50


class BulletSprite(arcade.Sprite):
    def __init__(self, bullet_path: str, speed: int, direction: str, game_window, client_ip, server_ip):
        super().__init__(bullet_path)
        self.client_ip = client_ip
        self.server_ip = server_ip
        self.game = game_window
        self.speed = speed
        self.height = 100
        self.width = 100
        self.actions = {
            arcade.key.UP: False,
            arcade.key.DOWN: False,
            arcade.key.LEFT: False,
            arcade.key.RIGHT: False
        }
        self.other_players = {}
        self.direction = direction

    def move(self):
        if self.direction == "Right":
            self.center_x += self.speed
        elif self.direction == "Left":
            self.center_x -= self.speed
        elif self.direction == "Up":
            self.center_y += self.speed
        elif self.direction == "Down":
            self.center_y -= self.speed


class EnemySprite(arcade.AnimatedTimeBasedSprite):
    def __init__(self, path: str, scale: float, center_x: int, center_y: int):
        super().__init__(path)
        self.path = path
        self.scale = scale
        self.center_x = center_x
        self.center_y = center_y

    def createEnemy(self, path: pathlib, scale: float, center_x: int, center_y: int):
        enemy = arcade.AnimatedTimeBasedSprite(scale=scale, center_x=center_x, center_y=center_y)
        all_files = path.glob('*.png')
        textures = []
        for file_path in all_files:
            frame = arcade.AnimationKeyframe(100, 120, arcade.load_texture(str(file_path)))
            textures.append(frame)
        enemy.frames = textures
        return enemy


class Client(arcade.Window):
    def __init__(self):
        super().__init__(960, 960, "Initial Tiled Map Super Simple Example")
        self.enemy_bullet_list = None
        self.enemy2_path = pathlib.Path.cwd() / 'Assets' / 'big_brown_zombie'
        self.enemy3_path = pathlib.Path.cwd() / 'Assets' / 'muddy_zombie'
        self.enemy4_path = pathlib.Path.cwd() / 'Assets' / 'ogre'
        self.map_location = pathlib.Path.cwd() / 'Assets' / 'DemoClassMap.json'
        self.current_scene = None
        self.mapscene1 = None
        self.mapscene2 = None
        self.mapscene3 = None
        self.wall_list = None
        self.fire_wall = None
        self.wall_list2 = None
        self.wall_list3 = None
        self.player: arcade.AnimatedWalkingSprite = None
        self.bullet_path = pathlib.Path.cwd() / 'Assets' / 'bullet_shot.png'
        self.bullet_sprite = BulletSprite(str(self.bullet_path), speed=3, direction="Right".lower(), game_window=self)
        self.bullet_list = None
        self.enemy1_path = pathlib.Path.cwd() / 'Assets' / 'zombie_big_run_anim'
        self.enemy1: arcade.AnimatedTimeBasedSprite = None
        self.enemy2: arcade.AnimatedTimeBasedSprite = None
        self.enemy3: arcade.AnimatedTimeBasedSprite = None
        self.enemy1_list: arcade.SpriteList = None
        self.non_moving_enemies: arcade.SpriteList = None
        self.simple_physics = None
        self.simple_physics1 = None
        self.simple_physics2 = None
        self.simple_physics3 = None
        self.simple_phy_mp2_enem2 = None
        self.simple_phy_mp2_enem1 = None
        self.health_list = None
        self.player_list: arcade.SpriteList = None
        self.move_speed = 2.5
        self.enemy1_move_speed = 1.5
        self.enemy2_move_speed = 1.5
        self.prev_scene: arcade.Scene = None
        self.health_path = pathlib.Path.cwd() / 'Assets' / 'fullheart.png'
        self.score = 0
        self.last_score = 0
        self.path = None
        self.display_points = ""
        self.enemy_movement_x = 1.5
        self.enemy_movement_y = self.enemy_movement_x
        self.map2_enem_list = None
        self.map2_enem_list_NM = None
        self.backgroundm_path = pathlib.Path.cwd() / 'Assets' / 'background_music.mp3'
        self.background_sound = None
        self.shoot_sound_path = pathlib.Path.cwd() / 'Assets' / 'shoot_sound.wav'
        self.dead_sound_path = pathlib.Path.cwd() / 'Assets' / 'dead_sound.wav'
        self.dead_sound = None
        self.enemy_voice_sound = None
        self.enemy_voice_path = pathlib.Path.cwd() / 'Assets' / 'enemy_voice.wav'
        self.lights_flickering_sound = None
        self.lights_sound_path = pathlib.Path.cwd() / 'Assets' / 'light_bulb.wav'
        self.run_sound_path = pathlib.Path.cwd() / 'Assets' / 'foot_steps.mp3'
        self.run_sound = None
        self.last_lvl_spath = pathlib.Path.cwd() / 'Assets' / 'last_level.wav'
        self.last_lvl_sound = None
        self.player_dying_sound = None
        self.player_dying_path = pathlib.Path.cwd() / 'Assets' / 'player_dying.wav'

    def setup(self):
        sample_map = arcade.tilemap.load_tilemap(self.map_location)
        self.mapscene1 = arcade.Scene.from_tilemap(sample_map)
        self.wall_list = sample_map.sprite_lists["WallLayer"]
        map2 = arcade.tilemap.load_tilemap(pathlib.Path.cwd() / 'Assets' / 'Map2.json')
        self.mapscene2 = arcade.Scene.from_tilemap(map2)
        #map3 = arcade.tilemap.load_tilemap(pathlib.Path.cwd() / 'Assets' / 'Map3.json')
        #self.mapscene3 = arcade.Scene.from_tilemap(map3)
        self.wall_list2 = map2.sprite_lists['wallLayer']
        #self.wall_list3 = map3.sprite_lists['wallLayer']
        player_path = pathlib.Path.cwd() / 'Assets' / 'new.png'
        self.player = arcade.AnimatedWalkingSprite(scale=1.8, center_x=780, center_y=780)
        frame = arcade.load_texture(str(player_path), 0, FRAME_HEIGHT, height=FRAME_HEIGHT,
                                    width=FRAME_WIDTH)
        self.player.stand_left_textures = []
        self.player.stand_left_textures.append(frame)
        frame = arcade.load_texture(str(player_path), 0, 0, height=FRAME_HEIGHT, width=FRAME_WIDTH)
        self.player.stand_right_textures = []
        self.player.stand_right_textures.append(frame)
        self.player.texture = frame
        self.player.walk_right_textures = []
        self.player.walk_left_textures = []
        for image_num in range(8):
            frame = arcade.load_texture(str(player_path), image_num * FRAME_WIDTH, 0, height=FRAME_HEIGHT,
                                        width=FRAME_WIDTH)
            self.player.walk_right_textures.append(frame)
        for image_num in range(8):
            frame = arcade.load_texture(str(player_path), image_num * FRAME_WIDTH, FRAME_HEIGHT, height=FRAME_HEIGHT,
                                        width=FRAME_WIDTH)
            self.player.walk_left_textures.append(frame)
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        self.bullet_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.health_list = arcade.SpriteList()

        adjustment = 0
        for count in range(3):
            health_sprite = arcade.Sprite(str(self.health_path))
            health_sprite.center_y = 30
            health_sprite.center_x = 750 + adjustment
            self.health_list.append(health_sprite)
            adjustment += 60
        self.enemy1_list = arcade.SpriteList()
        self.enemy1 = Client.createEnemy(self, enemy_path=self.enemy2_path, scale=3, center_y=360, center_x=100)
        self.simple_physics1 = arcade.PhysicsEngineSimple(self.enemy1, self.wall_list)
        self.enemy1_list.append(self.enemy1)
        self.simple_physics = arcade.PhysicsEngineSimple(self.player, self.wall_list)
        self.current_scene = self.mapscene1
        self.enemy2 = Client.createEnemy(self, enemy_path=self.enemy4_path, scale=3, center_y=630, center_x=100)
        self.simple_physics2 = arcade.PhysicsEngineSimple(self.enemy2, self.wall_list)
        self.enemy2_list = arcade.SpriteList()
        self.enemy1_list.append(self.enemy2)
        self.non_moving_enemies = arcade.SpriteList()
        self.enemy3 = Client.createEnemy(self, enemy_path=self.enemy1_path, scale=3.8, center_y=220, center_x=500)
        self.simple_physics3 = arcade.PhysicsEngineSimple(self.enemy3, self.wall_list)
        self.enemy4 = Client.createEnemy(self, enemy_path=self.enemy3_path, scale=3.8, center_y=780, center_x=500)
        self.non_moving_enemies.append(self.enemy3)
        self.non_moving_enemies.append(self.enemy4)
        self.mapscene1.add_sprite_list("enemies", sprite_list=self.enemy1_list)
        self.mapscene1.add_sprite_list("dumb_enemies", sprite_list=self.non_moving_enemies)
        self.map2_enem_list_NM = arcade.SpriteList()
        self.map2_enem_list = arcade.SpriteList()
        self.map2_enem1 = Client.createEnemy(self, enemy_path=self.enemy2_path, scale=3.8, center_y=780,
                                             center_x=450)
        self.map2_enem2 = Client.createEnemy(self, enemy_path=self.enemy2_path, scale=3.8, center_y=200,
                                             center_x=200)
        self.map2_enem3 = Client.createEnemy(self, enemy_path=self.enemy2_path, scale=3.8, center_y=200,
                                             center_x=780)
        self.map2_enem4 = Client.createEnemy(self, enemy_path=self.enemy2_path, scale=3.8, center_y=220,
                                             center_x=500)
        self.simple_phy_mp2_enem2 = arcade.PhysicsEngineSimple(self.map2_enem2, self.wall_list2)
        self.simple_phy_mp2_enem1 = arcade.PhysicsEngineSimple(self.map2_enem1, self.wall_list2)
        self.map2_enem_list.append(self.map2_enem1)
        self.map2_enem_list.append(self.map2_enem2)
        self.map2_enem_list_NM.append(self.map2_enem3)
        self.map2_enem_list_NM.append(self.map2_enem4)
        self.mapscene2.add_sprite_list("enemies", sprite_list=self.map2_enem_list)
        self.mapscene2.add_sprite_list('dumb_enemies', sprite_list=self.map2_enem_list_NM)
        self.background_sound = arcade.load_sound(self.backgroundm_path)
        arcade.play_sound(self.background_sound, looping=True)
        self.shoot_sound = arcade.load_sound(self.shoot_sound_path)
        self.dead_sound = arcade.load_sound(self.dead_sound_path)
        self.enemy_voice_sound = arcade.load_sound(self.enemy_voice_path)
        self.lights_flickering_sound = arcade.load_sound(self.lights_sound_path)
        self.run_sound = arcade.load_sound(self.run_sound_path)
        self.last_lvl_sound = arcade.load_sound(self.last_lvl_spath)
        self.player_dying_sound = arcade.load_sound(self.player_dying_path)

    def on_draw(self):
        arcade.start_render()
        self.current_scene.draw()
        self.player_list.draw()
        self.health_list.draw()
        arcade.draw_text(f"Score: {self.score}", 50, 20, arcade.color.WHITE, font_size=35, width=200)
        self.mapscene1.get_sprite_list("enemies").draw()
        self.mapscene1.get_sprite_list('dumb_enemies').draw()
        self.mapscene2.get_sprite_list('enemies')
        self.mapscene2.get_sprite_list('dumb_enemies')

        current_enemies_moving = self.current_scene.get_sprite_list("dumb_enemies")
        for enemy in current_enemies_moving:
            if enemy == self.enemy3:
                enemy.center_x += self.enemy1_move_speed
                if enemy.center_x <= 420:
                    self.enemy1_move_speed = 1.5

                elif enemy.center_x >= 820:
                    self.enemy1_move_speed = -1.5

            elif enemy == self.enemy4:
                enemy.center_x += self.enemy2_move_speed
                if enemy.center_x <= 110:
                    self.enemy2_move_speed = 1.5
                elif enemy.center_x >= 520:
                    self.enemy2_move_speed = -1.5

        current_enemies = self.current_scene.get_sprite_list("enemies")
        for enemy in current_enemies:
            dist_btwn_entity = dist((self.player.center_x, self.player.center_y), (enemy.center_x, enemy.center_y))
            if dist_btwn_entity <= 300:
                new_bullet = BulletSprite(str(self.bullet_path), speed=3, direction="Right".lower(), game_window=self)
                new_bullet.center_x = enemy.center_x
                new_bullet.center_y = enemy.center_y
                bullet_direction = ""
                if self.player.center_x < enemy.center_x:
                    enemy.center_x -= 1.5
                    bullet_direction = "Left"

                else:
                    enemy.center_x += 1.5
                    bullet_direction = "Right"
                newer_bullet = BulletSprite(str(self.bullet_path), speed=3, direction="Right".lower(), game_window=self)
                newer_bullet.center_x = enemy.center_x
                newer_bullet.center_y = enemy.center_y
                new_bullet.direction = bullet_direction
                if random.randrange(1, 250) == 10:
                    self.enemy_bullet_list.append(new_bullet)
                    arcade.play_sound(self.enemy_voice_sound)

                if self.player.center_y < enemy.center_y:
                    enemy.center_y -= 1.5
                    newer_bullet.direction = "Down"
                else:
                    enemy.center_y += 1.5
                    newer_bullet.direction = "Up"

                if random.randrange(1, 250) == 10:
                    self.enemy_bullet_list.append(newer_bullet)

            if enemy.collides_with_list(self.wall_list):
                if enemy in current_enemies:
                    # current_enemies.remove(enemy)
                    pass

        self.last_score = 0
        if self.score != self.last_score:
            self.last_score = self.score

        for bullet in self.enemy_bullet_list:
            bullet.draw()
            bullet.move()
        for bullet in self.bullet_list:
            bullet.draw()
            bullet.move()

    def createEnemy(self, enemy_path: Path, scale: float, center_x: int, center_y: int):
        enemy = arcade.AnimatedTimeBasedSprite(scale=scale, center_x=center_x, center_y=center_y)
        all_files = enemy_path.glob('*.png')
        textures = []
        for file_path in all_files:
            frame = arcade.AnimationKeyframe(100, 135, arcade.load_texture(str(file_path)))
            textures.append(frame)
        enemy.frames = textures
        enemy.hit_box = [[-10, -10], [10, -10], [10, 10]]
        return enemy

    def on_update(self, delta_time: float):
        self.current_scene.update()
        self.mapscene2.update()
        self.mapscene1.update()
        self.simple_physics.update()
        self.simple_physics1.update()
        self.simple_physics2.update()
        self.simple_physics3.update()
        self.simple_phy_mp2_enem1.update()
        self.simple_phy_mp2_enem2.update()
        self.player_list.update()
        self.player_list.update_animation()
        for enemy in self.enemy1_list:
            enemy.update_animation()
        for enemy in self.non_moving_enemies:
            enemy.update_animation()
        for enemy in self.map2_enem_list:
            enemy.update_animation()
        for enemy in self.map2_enem_list_NM:
            enemy.update_animation()

        for player in self.player_list:
            collision_with_enemy1 = arcade.check_for_collision_with_list(player,
                                                                         self.mapscene1.get_sprite_list('enemies'))
            collision_with_enemy2 = arcade.check_for_collision_with_list(player,
                                                                         self.mapscene1.get_sprite_list('dumb_enemies'))
            if len(collision_with_enemy1) == 1:
                self.player_list.remove(player)
                arcade.play_sound(self.player_dying_sound)
                self.player.center_x = 780
                self.player.center_y = 780
                self.player_list.append(self.player)
                if len(self.health_list) != 1:
                    self.health_list.pop(-1)
                else:
                    exit(0)
            if len(collision_with_enemy2) == 1:
                self.player_list.remove(player)
                arcade.play_sound(self.player_dying_sound)
                self.player.center_x = 780
                self.player.center_y = 780
                self.player_list.append(self.player)
                if len(self.health_list) != 1:
                    self.health_list.pop(-1)
                else:
                    exit(0)
        for bullet in self.bullet_list:
            collision_with_enemy = arcade.check_for_collision_with_list(bullet,
                                                                        self.mapscene1.get_sprite_list('enemies'))
            collision_with_enemy2 = arcade.check_for_collision_with_list(bullet,
                                                                         self.mapscene1.get_sprite_list('dumb_enemies'))
            collision_with_walls = arcade.check_for_collision_with_list(bullet, self.wall_list)
            if len(collision_with_enemy) == 1:
                self.bullet_list.remove(bullet)
                self.current_scene.get_sprite_list('enemies').remove(collision_with_enemy[0])
                self.score += 100
                arcade.play_sound(self.dead_sound, volume=200)
            if len(collision_with_enemy2) == 1:
                self.bullet_list.remove(bullet)
                self.current_scene.get_sprite_list('dumb_enemies').remove(collision_with_enemy2[0])
                self.score += 100
                arcade.play_sound(self.dead_sound, volume=200)

            if len(collision_with_walls) == 1:
                self.bullet_list.remove(bullet)
        for bullet in self.enemy_bullet_list:
            collision_with_walls = arcade.check_for_collision_with_list(bullet, self.wall_list)
            collision_with_players = arcade.check_for_collision_with_list(bullet, self.player_list)
            if len(collision_with_walls) == 1:
                self.enemy_bullet_list.remove(bullet)
            elif len(collision_with_players) == 1:
                self.player_list.remove(self.player)
                arcade.play_sound(self.player_dying_sound)
                self.enemy_bullet_list.remove(bullet)
                self.player.center_x = 780
                self.player.center_y = 780
                self.player_list.append(self.player)
                if len(self.health_list) != 1:
                    self.health_list.pop(-1)
                else:
                    exit(0)
        for enemy in self.current_scene.get_sprite_list('enemies'):
            enemy_collides_wall = arcade.check_for_collision_with_list(enemy, self.wall_list)
            if len(enemy_collides_wall) == 1:
                # self.current_scene.get_sprite_list('enemies').remove(enemy_collides_wall[0])
                pass

    def on_key_press(self, key: int, modifiers: int):
        if (key in self.actions.keys):
            self.actions.keys[key] = True

    def on_key_release(self, symbol: int, modifiers: int):
        if (symbol in self.actions.keys):
            self.actions.keys[symbol] = False

def setup_client_connection(client: Client):
    client_event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(client_event_loop)
    client_event_loop.create_task(communication_with_server(client, client_event_loop))
    client_event_loop.run_forever()

async def communication_with_server(client: Client, event_loop):
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    while True:
        keystate = json.dumps(client.actions.keys)
        x_loc = player_info.x_loc + 1* client.player.actions(arcade.key.RIGHT) - 1* client.player.actions(arcade.key.RIGHT)
        y_loc = player_info.y_loc + 1* client.player.actions(arcade.key.UP) - 1* client.player.actions(arcade.key.DOWN)
        player_position = PlayerLocation(x_loc, y_loc)
        UDPClientSocket.sendto(str.encode(player_position), (client.ip, Server.SERVER_PORT))
        data_packet = UDPClientSocket.recvfrom(1024)
        data = data_packet[0]  # get the encoded string
        decoded_data: PlayerLocation.GameState = PlayerLocation.GameState.from_json(data)
        player_dict = decoded_data.player_states
        player_info = player_dict[client.ip_addr]
        client.player.center_x = player_info.x_loc + 1* client.player.actions(arcade.key.RIGHT) - 1* client.player.actions(arcade.key.RIGHT)
        client.player.center_y = player_info.y_loc + 1* client.player.actions(arcade.key.UP) - 1* client.player.actions(arcade.key.DOWN)
        for ip in player_dict:
            if (ip != client.ip_addr):
                if(ip not in client.other_players):
                    client.other_players.append(arcade.Sprite(pathlib.Path.cwd() / 'Assets' / 'big_brown_zombie'))
                client.other_players[ip].center_x = player_dict[ip].x_loc
                client.other_players[ip].center_y = player_dict[ip].y_loc

