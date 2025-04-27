from ursina import *
from player import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()



# Инициализация игрока ДО других объектов
player = Player(
    position=(3, 3, 3),
    gravity=0.5,
    normal_speed=6,
    collider='mesh',
    jump_height=0.77,
    air_control=0.5
)

enemy = AdvancedEnemy(position=(5, 0, 5))

# карта
map_entity = Entity(
    model='textures/de_dust2.obj',
    collider='mesh',
    texture='white_cube',
    scale=0.03,
    rotation=(-90,0,0),
    position=(25, 0, 0),
    double_sided=True  # Важно для внутренних поверхностей!
)
map_entity.combine()

#рука
hand = Entity(
    parent=camera.ui,
    model='arm',
    texture='arm_tex',
    scale=0.23,
    position=Vec3(0.63, -0.34, -0.1),
    rotation=Vec3(0, -200, 10)
)

#оружие
gun = Entity(
    parent=camera.ui,
    model='USP',
    texture='dirty-metal-texture',
    scale=0.07,
    position=Vec3(0.4, -0.3, 0.27),
    rotation=Vec3(0, -200, 10)
)



DirectionalLight(position=(10, 20, -10), shadows=True)
AmbientLight(color=color.gray)

app.run()
