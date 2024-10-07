import bpy
import os
import numpy as np
from mathutils import Quaternion

# Основной путь для рендеров (вы указываете вручную)
main_save_path = r"D:\0_filesys\3_Library\Prj\CNN AntiDrone\DS_drone\Render"

# Списки коллекций для активации вместе с объектом для рендера
collection1 = (['ENV_D1', 'D1', 'D1_60'], 'D1_60_2')
collection2 = (['ENV_D1', 'D1', 'D1_82'], 'D1_82')
#collection2 = (['ENV_D2', 'D2', 'D2_60'], 'obj_in_D2')

collections_to_activate = [
    (collection1, r"D:\0_filesys\3_Library\Prj\CNN AntiDrone\DS_drone\Render\D1_60_2"),
    (collection2, r"D:\0_filesys\3_Library\Prj\CNN AntiDrone\DS_drone\Render\D1_82"),
]

# Функция для управления видимостью коллекций
def toggle_collections(collection_names, visible):
    for collection in bpy.data.collections:
        if collection.name in collection_names:
            collection.hide_render = not visible

# Функция для поиска объекта в коллекции
def find_object_in_collection(collection_name, object_name):
    collection = bpy.data.collections.get(collection_name)
    if collection:
        for obj in collection.objects:
            if obj.name == object_name:
                return obj
    return None

# Функция для рендеринга сцены с текущими параметрами
def render_scene(output_path, file_name):
    bpy.context.scene.render.filepath = os.path.join(output_path, file_name)
    bpy.ops.render.render(write_still=True)

# Функция для создания кватерниона из угла поворота вокруг оси
def create_quaternion(axis, angle):
    if axis == 'x':
        return Quaternion((np.cos(angle / 2), np.sin(angle / 2), 0, 0))
    elif axis == 'y':
        return Quaternion((np.cos(angle / 2), 0, np.sin(angle / 2), 0))
    elif axis == 'z':
        return Quaternion((np.cos(angle / 2), 0, 0, np.sin(angle / 2)))
    return Quaternion((1, 0, 0, 0))

# Задаем шаг для изменения кватерниона и диапазон от -1 до 1
step = 0.5
quaternion_range = np.arange(-1, 1 + step, step)

# Подсчитываем количество комбинаций вращений
total_combinations = len(quaternion_range) ** 3 * 3  # вращения по 3 осям

# Основной цикл по комбинациям коллекций
for (collection, object_name), save_folder in collections_to_activate:
    # Создаем отдельную папку для рендеров текущей коллекции
    collection_save_path = os.path.join(main_save_path, save_folder)
    if not os.path.exists(collection_save_path):
        os.makedirs(collection_save_path)
    
    # Включаем текущую коллекцию для рендера
    toggle_collections(collection, True)
    
    # Находим объект для вращения в текущей коллекции
    obj = find_object_in_collection(collection[-1], object_name)
    
    if obj is None:
        print(f"Объект '{object_name}' не найден в коллекции '{collection[-1]}'")
        continue
    
    # Сохраняем начальное вращение объекта
    initial_rotation = obj.rotation_quaternion.copy()
    
    combination_counter = 0
    
    # Цикл для вращений по осям x, y, z для текущей коллекции
    for axis in ['x', 'y', 'z']:
        for angle in quaternion_range:
            # Создаем кватернион для поворота
            rotation_quat = create_quaternion(axis, angle * np.pi)  # Применяем угол в радианах
            
            # Применяем кватернион к начальному вращению объекта
            obj.rotation_quaternion = initial_rotation @ rotation_quat
            
            # Генерируем имя файла для рендера
            file_name = f'render_{axis}_{round(angle, 2)}.png'
            
            # Выполняем рендер и сохраняем изображение
            render_scene(collection_save_path, file_name)
            
            # Счётчик комбинаций
            combination_counter += 1
            print(f"Рендер {combination_counter}/{total_combinations} завершен для коллекции {save_folder}: {file_name}")
    
    # Отключаем текущую коллекцию после рендеринга
    toggle_collections(collection, False)

    # Восстанавливаем исходное вращение объекта
    obj.rotation_quaternion = initial_rotation
