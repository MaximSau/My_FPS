from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# Класс врага
class Enemy(Entity):
    def __init__(self, position):
        super().__init__(
            model='cube',
            color=color.red,
            scale=(1, 2, 1),
            position=position,
            collider='box'
        )

    def take_damage(self):
        destroy(self)  # Уничтожаем врага при попадании


class Bullet(Entity):
    def __init__(self, position, direction):
        super().__init__(
            model='sphere',
            color=color.red,
            scale=0.2,
            position=position,
            collider='sphere'
        )
        self.direction = direction.normalized()
        self.speed = 30  # Увеличена скорость
        self.creation_time = time.time()

    def update(self):
        self.position += self.direction * self.speed * time.dt

        # Проверка столкновений (игнорируем игрока)
        hit_info = self.intersects(ignore=[self, Player])
        if hit_info.hit and isinstance(hit_info.entity, Enemy):
            hit_info.entity.take_damage()
            destroy(self)

        if time.time() - self.creation_time > 2:
            destroy(self)


class AdvancedEnemy(Enemy):
    def __init__(self, position):
        super().__init__(position)
        self.health = 100  # Добавляем здоровье

    def take_damage(self):
        self.health -= 50
        if self.health <= 0:
            destroy(self)


class Player(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Настройки коллайдера и управления
        self.collider = BoxCollider(self, size=(1, 2, 1))
        self.mouse_sensitivity = Vec2(50, 50)

        # Параметры скорости
        self.normal_speed = 7.0
        self.crouch_speed = 3.5


        # Настройка курсора
        self.cursor = Entity(
            parent=camera.ui,
            model='quad',
            color=color.white33,
            scale=(0.008, 0.03),
            rotation_z=45
        )

        self.gun = Entity(
            parent=self.camera_pivot,
            model='cube',
            scale=(0.1, 0.5, 0.1),
            position=(0.5, -0.5, 1),
            rotation=(0, 0, 45)
        )

    def input(self, key):
        super().input(key)
        if key == 'escape':
            application.quit()
        if key == 'left mouse down':
            # Позиция и направление из камеры
            camera_pos = self.camera_pivot.world_position
            camera_forward = self.camera_pivot.forward
            spawn_pos = camera_pos + camera_forward * 1.5

            # Создание пули
            bullet = Bullet(spawn_pos, camera_forward)


    def update(self):
        super().update() # Вызываем родительский update

        if held_keys['shift']:
            self.speed = self.crouch_speed + 0.8
        elif held_keys['control']:
            self.speed = self.crouch_speed
            self.collider.size = (1, 1.3, 1)
        else:
            self.speed = self.normal_speed
            self.collider.size = (1, 2, 1)  # Возвращаем исходный размер

        if self.y < -10:
            self.position = (0, 2, 0)
