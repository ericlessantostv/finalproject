def on_key_press(self, key: int, modifiers: int):
    if key == arcade.key.UP:
        self.actions[key] = True
        # self.player.change_y = self.move_speed
        self.player.direction = "Up"
        arcade.play_sound(self.run_sound)

    if key == arcade.key.DOWN:
        self.player.change_y = -self.move_speed
        self.player.direction = "Down"
        arcade.play_sound(self.run_sound)

    if key == arcade.key.LEFT:
        self.player.change_x = -self.move_speed
        self.player.direction = "Left"
        arcade.play_sound(self.run_sound)

    if key == arcade.key.RIGHT:
        self.player.change_x = self.move_speed
        self.player.direction = "Right"
        arcade.play_sound(self.run_sound)

    if key == arcade.key.SPACE:
        player_direction = self.player.direction
        bullet = BulletSprite(str(self.bullet_path), speed=10, direction=player_direction, game_window=self)
        start_x = self.player.center_x
        start_y = self.player.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y
        self.bullet_list.append(bullet)
        arcade.play_sound(self.shoot_sound)
    number_of_enemies_left = len(self.mapscene1.get_sprite_list('enemies')) + len(
        self.mapscene1.get_sprite_list('dumb_enemies'))
    print("number:" + str(number_of_enemies_left))
    if self.player.center_x < -2 and number_of_enemies_left == 0:  # if the player is on map1 and heading off the map
        self.current_scene = self.mapscene2
        arcade.play_sound(self.lights_flickering_sound)
        self.player.center_x = self.width - self.player.width / 2
        self.simple_physics = arcade.PhysicsEngineSimple(self.player, self.wall_list2)
    elif self.player.center_x < -2 and number_of_enemies_left > 0:
        self.player.center_x = 20
    elif self.player.center_x > self.width + 2:  # if we are on map2 and headed off the scene
        self.current_scene = self.mapscene1
        self.player.center_x = self.player.width / 2
        self.simple_physics = arcade.PhysicsEngineSimple(self.player, self.wall_list)
    if self.player.center_y > self.height + 2:
        self.current_scene = self.mapscene3
        arcade.play_sound(self.last_lvl_sound)
        # self.current_scene.add_sprite_list()
        self.player.center_y = 20
        self.simple_physics = arcade.PhysicsEngineSimple(self.player, self.wall_list3)
    elif self.player.center_y < - 2:
        self.current_scene = self.mapscene2
        self.player.center_y = 900
        self.simple_physics = arcade.PhysicsEngineSimple(self.player, self.wall_list2)

    def on_key_release(self, key: int, modifiers: int):
        if self.player.change_y < 0 and (key == arcade.key.DOWN or key == arcade.key.S):
            self.player.change_y = 0

        if self.player.change_y > 0 and (key == arcade.key.UP or key == arcade.key.W):
            self.player.change_y = 0

        if self.player.change_x < 0 and (key == arcade.key.LEFT or key == arcade.key.A):
            self.player.change_x = 0

        if self.player.change_x > 0 and (key == arcade.key.RIGHT or key == arcade.key.D):
            self.player.change_x = 0