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
        'x' : axis[0],
        'y' : axis[1],
        'z' : axis[2]
    }

def axis_angle_dict(axis, angle):
    return {
        'axis' : vect3_dict(axis),
        'angle' : angle
    }

def camera_dict(cam):
    m = cam.matrix_world
    (axis, angleRad) = m.to_quaternion().to_axis_angle()
    return {
        'fov' : degrees(cam.data.angle),
        'translation' : vect3_dict(m.translation),
        'rotation' : axis_angle_dict(axis, degrees(angleRad))
    }

def meshvertex_dict(vertex):
    return {
        'co' : vect3_dict(vertex.co),
        'normal' : vect3_dict(vertex.normal)
    }

def matrixworld_dict(m):
    # just flattening out the matrix m into row-major
    ls = list(map(list, list(m.row)))
    return [item for sublist in ls for item in sublist]

def meshpolygon_dict(polygon):
    return list(polygon.vertices)

def mesh_dict(matrixworld, mesh):
    return {
        'matrixWorld' : matrixworld_dict(matrixworld),
        'vertices' : list(map(meshvertex_dict, mesh.vertices)),
        'faces' : list(map(meshpolygon_dict, mesh.polygons))
    }

def mesh_ob_dict(ob, scene):
    mesh = ob.to_mesh(scene, True, 'RENDER')
    return {
        'name' : ob.name,
        'mesh' : mesh_dict(ob.matrix_world, mesh)
    }

def scene_dict(width, height, scene):
    resfac = scene.render.resolution_percentage / 100.0
    return {
        'camera' : camera_dict(scene.camera),
        'xres' : width,
        'yres' : height
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
        # scene.frame_set(1, 0.0)
        # Create the scene
        resfac = scene.render.resolution_percentage / 100.0
        self.width  = int(scene.render.resolution_x * resfac)
        self.height = int(scene.render.resolution_y * resfac)
        jscene = scene_dict(self.width, self.height, scene)

        # Create objects list
        jobjs = []
        for ob in scene.objects:
            # TODO: check if object is visible for rendering
            # TODO: proper object instancing
            if ob.type == 'MESH':
                jobjs.append(mesh_ob_dict(ob, scene))

        # Compose scene and objects list into top-level blob
        blob = {
            'scene': jscene,
            'objects': jobjs
        }
        print(json.dumps(blob, sort_keys=True))

        # set result
        result = self.begin_result(0, 0, self.width, self.height)
        rpass = result.layers[0].passes[0]
        rpass.rect = [ [0.0, 0.0, 1.0, 1.0] ] * (self.width * self.height)
        self.end_result(result)

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
