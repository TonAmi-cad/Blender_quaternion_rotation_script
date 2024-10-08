import bpy
import os
import numpy as np
from mathutils import Quaternion

# Path for saving renders and text files
save_path = r"full_path_to_output_folder"

if not os.path.exists(save_path):
    os.makedirs(save_path)

# Set step for changing quaternion
step = 0.1

# Define range for quaternions
quaternion_range = np.arange(-1, 1 + step, step)

# Function to create quaternion from rotation angle around axis
def create_quaternion(axis, angle):
    if axis == 'x':
        q = Quaternion((np.cos(angle / 2), np.sin(angle / 2), 0, 0))
    elif axis == 'y':
        q = Quaternion((np.cos(angle / 2), 0, np.sin(angle / 2), 0))
    elif axis == 'z':
        q = Quaternion((np.cos(angle / 2), 0, 0, np.sin(angle / 2)))
    else:
        q = Quaternion((1, 0, 0, 0))
    
    # Normalize the quaternion
    q.normalize()
    
    return q

# Get the active object
obj = bpy.context.active_object

# Save the initial rotation of the object
initial_rotation = Quaternion((1, 0, 0, 0))

# First render without rotation
combination_counter = 0
obj.rotation_quaternion = initial_rotation

# Update the scene and render the first image without rotation
bpy.context.view_layer.update()

# Name for render file and text file
file_name = f"render_{combination_counter:05d}"

# Save the render
bpy.context.scene.render.filepath = os.path.join(save_path, f"{file_name}.png")
bpy.ops.render.render(write_still=True)

# Save quaternion parameters in a text file
quat = obj.rotation_quaternion
with open(os.path.join(save_path, f"{file_name}.txt"), "w") as f:
    f.write(f"Quaternion (w, x, y, z): {quat.w}, {quat.x}, {quat.y}, {quat.z}\n")

# Transition to rendering rotations around axes (first X, then Y, then Z)
combination_counter += 1

# Rotations around the X axis
for angle in quaternion_range:
    rotation_quat = create_quaternion('x', angle * np.pi)
    obj.rotation_quaternion = initial_rotation @ rotation_quat
    
    # Normalize the object's quaternion after applying rotation
    obj.rotation_quaternion.normalize()
    
    # Update the scene
    bpy.context.view_layer.update()

    # Name for render file and text file
    file_name = f"render_{combination_counter:05d}"
    bpy.context.scene.render.filepath = os.path.join(save_path, f"{file_name}.png")
    bpy.ops.render.render(write_still=True)

    quat = obj.rotation_quaternion
    with open(os.path.join(save_path, f"{file_name}.txt"), "w") as f:
        f.write(f"Quaternion (w, x, y, z): {quat.w}, {quat.x}, {quat.y}, {quat.z}\n")

    combination_counter += 1

# Rotations around the Y axis
for angle in quaternion_range:
    rotation_quat = create_quaternion('y', angle * np.pi)
    obj.rotation_quaternion = initial_rotation @ rotation_quat
    
    # Normalize the object's quaternion after applying rotation
    obj.rotation_quaternion.normalize()

    # Update the scene
    bpy.context.view_layer.update()

    # Name for render file and text file
    file_name = f"render_{combination_counter:05d}"
    bpy.context.scene.render.filepath = os.path.join(save_path, f"{file_name}.png")
    bpy.ops.render.render(write_still=True)

    quat = obj.rotation_quaternion
    with open(os.path.join(save_path, f"{file_name}.txt"), "w") as f:
        f.write(f"Quaternion (w, x, y, z): {quat.w}, {quat.x}, {quat.y}, {quat.z}\n")

    combination_counter += 1

# Rotations around the Z axis
for angle in quaternion_range:
    rotation_quat = create_quaternion('z', angle * np.pi)
    obj.rotation_quaternion = initial_rotation @ rotation_quat
    
    # Normalize the object's quaternion after applying rotation
    obj.rotation_quaternion.normalize()

    # Update the scene
    bpy.context.view_layer.update()

    # Name for render file and text file
    file_name = f"render_{combination_counter:05d}"
    bpy.context.scene.render.filepath = os.path.join(save_path, f"{file_name}.png")
    bpy.ops.render.render(write_still=True)

    quat = obj.rotation_quaternion
    with open(os.path.join(save_path, f"{file_name}.txt"), "w") as f:
        f.write(f"Quaternion (w, x, y, z): {quat.w}, {quat.x}, {quat.y}, {quat.z}\n")

    combination_counter += 1

# Now combine rotations around all axes X, Y, Z
for x_angle in quaternion_range:
    for y_angle in quaternion_range:
        for z_angle in quaternion_range:
            # Create combined quaternion from angles around the X, Y, Z axes
            rotation_quat = create_quaternion('x', x_angle * np.pi) @ \
                            create_quaternion('y', y_angle * np.pi) @ \
                            create_quaternion('z', z_angle * np.pi)
            
            # Apply rotation
            obj.rotation_quaternion = initial_rotation @ rotation_quat
            
            # Normalize the object's quaternion after applying rotation
            obj.rotation_quaternion.normalize()

            # Update the scene
            bpy.context.view_layer.update()

            # Name for render file and text file
            file_name = f"render_{combination_counter:05d}"
            bpy.context.scene.render.filepath = os.path.join(save_path, f"{file_name}.png")
            bpy.ops.render.render(write_still=True)

            quat = obj.rotation_quaternion
            with open(os.path.join(save_path, f"{file_name}.txt"), "w") as f:
                f.write(f"Quaternion (w, x, y, z): {quat.w}, {quat.x}, {quat.y}, {quat.z}\n")

            combination_counter += 1
