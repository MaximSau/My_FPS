from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


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

    def input(self, key):
        super().input(key)  # Вызываем родительский input
        if key == 'escape':
            application.quit()
        if key == 'space':
            self.jump()

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
