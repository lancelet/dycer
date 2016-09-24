bl_info = {
    "name": "DycerBlend",
    "version": (0, 1),
    "author": "Jonathan Merritt",
    "blender": (2, 77, 0),
    "description": "Dycer renderer integration",
    "location": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Render"}

# Cycles stuff in: intern/cycles/blender/addon
# Fn-F8 reloads plugins

import bpy
import json

from math import degrees

dren = 'DYCER_RENDERER'

def vect3_dict(axis):
    return {
        'vec3' : {
            'x' : axis[0],
            'y' : axis[1],
            'z' : axis[2]
        }
    }

def axis_angle_dict(axis, angle):
    return {
        'axisangle' : {
            'axis' : vect3_dict(axis),
            'angle' : angle
        }
    }

def camera_dict(cam):
    m = cam.matrix_world
    (axis, angle) = m.to_quaternion().to_axis_angle()
    return {
        'camera' : {
            'fov' : degrees(cam.data.angle),
            'translation' : vect3_dict(m.translation),
            'rotation' : axis_angle_dict(axis, angle)
        }
    }

def scene_dict(scene):
    resfac = scene.render.resolution_percentage / 100.0
    return {
        'scene' : {
            'camera' : camera_dict(scene.camera),
            'xres' : scene.render.resolution_x * resfac,
            'yres' : scene.render.resolution_y * resfac
        }
    }

class DycerRender(bpy.types.RenderEngine):
    bl_idname = dren
    bl_label = "Dycer Render"
    bl_use_shading_nodes = False
    bl_use_preview = False
    bl_use_exclude_layers = True
    bl_use_save_buffers = False
    bl_use_spherical_stereo = False

    def render(self, scene):
        print("Render")
        print(json.dumps(scene_dict(scene), sort_keys=True))

    def update(self, data, scene):
        print("Update")

### UI STUFF

# Re-use some existing buttons in the renderer UI.

from bl_ui import properties_render
properties_render.RENDER_PT_render.COMPAT_ENGINES.add(dren)
properties_render.RENDER_PT_dimensions.COMPAT_ENGINES.add(dren)
del properties_render

from bl_ui import properties_data_camera
properties_data_camera.DATA_PT_lens.COMPAT_ENGINES.add(dren)
properties_data_camera.DATA_PT_camera.COMPAT_ENGINES.add(dren)
properties_data_camera.DATA_PT_camera_display.COMPAT_ENGINES.add(dren)
properties_data_camera.DATA_PT_custom_props_camera.COMPAT_ENGINES.add(dren)
del properties_data_camera


### Register

def register():
    bpy.utils.register_class(DycerRender)
    # bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_class(DycerRender)
    # bpy.utils.unregister_module(__name__)
