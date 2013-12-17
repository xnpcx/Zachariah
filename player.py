from character import *


class Player(Character):
    def __init__(self, lvl, loc, *groups):
        super(Character, self).__init__(*groups)
        self.sheet = pygame.image.load('images/char.png').convert_alpha()
        animTypes = 'idle_right walk_right run_right jump_right fall_right tred_right swim_right stop_right ' \
                    'damage_right'.split()
        self.placeholder = self.sheet.subsurface(0, 0, 32, 64)
        self.animSurf, self.hitmask_dict = self.get_images(self.sheet, animTypes, 32, 64)
        self.image = self.animSurf['idle_right'].getCurrentFrame()
        super(Player, self).__init__(lvl, loc)
        self.rect.center = loc
        
    def update(self, dt, lvl, key, joy):
        self.get_events(key, joy)
        self.check_keys(key, joy)
        self.inertia(key)
        super(Player, self).update(dt, lvl, key, joy)
        lvl.tilemap.set_focus(self.rect.centerx, self.rect.centery)
        self.max_speed = 3
        
    def check_keys(self, key, joy):
        #setting directions for idle
        x_vel = 0
        if self.dir == 'left':
            self.image = self.animSurf['idle_left'].getCurrentFrame()
            self.hitmask = self.hitmask_dict['idle_left'][self.animSurf['idle_left']._propGetCurrentFrameNum()]
        if self.dir == 'right':
            self.image = self.animSurf['idle_right'].getCurrentFrame()
            self.hitmask = self.hitmask_dict['idle_right'][self.animSurf['idle_right']._propGetCurrentFrameNum()]
        if self.run:
            self.max_speed = 6
        if self.direction == 'left':
            if abs(self.x_vel) > 1:
                self.image = self.animSurf['walk_left'].getCurrentFrame()
                self.hitmask = self.hitmask_dict['walk_left'][self.animSurf['walk_left']._propGetCurrentFrameNum()]
            if abs(self.x_vel) > 4:
                self.image = self.animSurf['run_left'].getCurrentFrame()
                self.hitmask = self.hitmask_dict['run_left'][self.animSurf['run_left']._propGetCurrentFrameNum()]
            self.dir = 'left'
            x_vel -= self.speed
        if self.direction == 'right':
            if self.x_vel > 1:
                self.image = self.animSurf['walk_right'].getCurrentFrame()
                self.hitmask = self.hitmask_dict['walk_right'][self.animSurf['walk_right']._propGetCurrentFrameNum()]
            if self.x_vel > 4:
                self.image = self.animSurf['run_right'].getCurrentFrame()
                self.hitmask = self.hitmask_dict['run_right'][self.animSurf['run_right']._propGetCurrentFrameNum()]
            self.dir = 'right'
            x_vel += self.speed
        self.x_vel += x_vel

    def inertia(self, key):
        max_speed = self.max_speed  # + abs(self.plat_speed)
        if abs(self.x_vel) - self.x_det > max_speed:
            if self.x_vel > 0:
                self.x_vel -= (self.x_det * 2)
            if self.x_vel < 0:
                self.x_vel += (self.x_det * 2)
        if self.x_vel > 0 and self.direction == '' or self.x_vel > max_speed:
            self.x_vel -= self.x_det
        if self.x_vel < 0 and self.direction == '' or self.x_vel < (max_speed * -1):
            self.x_vel += self.x_det
        #self.x_vel += self.plat_speed

    def get_events(self, key, joy):
        self.run = self.get_run(key, joy)
        self.direction = self.get_direction(key, joy)

    def get_direction(self, key, joy):
        direction = ''
        for event in joy:
            if event.get_hat(0) == (-1, 0):
                direction = 'left'
            elif event.get_hat(0) == (1, 0):
                direction = 'right'
        if key[pygame.K_LEFT]:
            direction = 'left'
        elif key[pygame.K_RIGHT]:
            direction = 'right'
        return direction

    def get_run(self, key, joy):
        run = False
        for event in joy:
            if event.get_button(2):
                run = True
        if key[pygame.K_LSHIFT]:
            run = True
        return run