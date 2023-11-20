bl_info = {
    "name": "Light Library",
    "blender": (2, 80, 0),
    "category": "Object",
    "author": "faizan",
    "description": "A simple light library add-on for Blender.",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Light Library > Light Library",
    "wiki_url": "https://github.com/faizan/your-addon",
    "tracker_url": "https://github.com/faizan/your-addon/issues",
    "support": "COMMUNITY",
}

import bpy

class OBJECT_PT_light_library(bpy.types.Panel):
    bl_label = "Light Library"
    bl_idname = "PT_OBJECT_PT_light_library"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tools'
    bl_context = 'objectmode'

    def draw(self, context):
        layout = self.layout

        lights = [obj for obj in bpy.context.scene.objects if obj.type == 'LIGHT']

        for light in lights:
            row = layout.row()
            row.label(text=light.name)

            split = row.split(factor=0.5)
            split.prop(light.data, "energy", text="Intensity")

            split = row.split(factor=0.7)
            split.prop(light.data, "color", text="Color")

            row = layout.row()
            op = row.operator("lighting.add_to_library", text="Add to Library")
            op.light_name = light.name

        row = layout.row()
        row.operator("lighting.load_default_setups", text="Load Default Setups")

        row = layout.row()
        row.operator("lighting.remove_all_presets", text="Remove All Presets")

        # Show light presets
        row = layout.row()
        row.label(text="Light Presets:")

        for preset in bpy.context.scene.light_library:
            row = layout.row()
            row.operator("lighting.add_preset_to_scene", text=preset.name).preset_name = preset.name

class OBJECT_OT_add_to_library(bpy.types.Operator):
    bl_idname = "lighting.add_to_library"
    bl_label = "Add Light to Library"
    bl_options = {'REGISTER', 'UNDO'}

    light_name: bpy.props.StringProperty()

    def execute(self, context):
        light = bpy.context.scene.objects.get(self.light_name)

        if light:
            # Create a new library item and store light properties
            library_item = bpy.context.scene.light_library.add()
            library_item.name = light.name
            library_item.energy = light.data.energy
            library_item.color = light.data.color
            library_item.light_type = light.data.type

        return {'FINISHED'}

class OBJECT_OT_load_default_setups(bpy.types.Operator):
    bl_idname = "lighting.load_default_setups"
    bl_label = "Load Default Light Setups"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Define default setups
        default_setups = [
            {"name": "Point Light", "energy": 200.0, "color": (1.0, 1.0, 1.0), "light_type": 'POINT'},
            {"name": "Spot Light", "energy": 100.0, "color": (0.5, 0.5, 0.5), "light_type": 'SPOT'},
            {"name": "Sun Light", "energy": 150.0, "color": (0.8, 0.2, 0.2), "light_type": 'SUN'},
        ]

        # Add default setups to the library
        for setup in default_setups:
            library_item = bpy.context.scene.light_library.add()
            library_item.name = setup["name"]
            library_item.energy = setup["energy"]
            library_item.color = setup["color"]
            library_item.light_type = setup["light_type"]

        return {'FINISHED'}

class OBJECT_OT_remove_all_presets(bpy.types.Operator):
    bl_idname = "lighting.remove_all_presets"
    bl_label = "Remove All Light Presets"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Clear the light library
        bpy.context.scene.light_library.clear()
        return {'FINISHED'}

class OBJECT_OT_add_preset_to_scene(bpy.types.Operator):
    bl_idname = "lighting.add_preset_to_scene"
    bl_label = "Add Light Preset to Scene"
    bl_options = {'REGISTER', 'UNDO'}

    preset_name: bpy.props.StringProperty()

    def execute(self, context):
        preset = bpy.context.scene.light_library.get(self.preset_name)

        if preset:
            # Create a new light object in the 3D scene based on the preset's light type
            bpy.ops.object.light_add(type=preset.light_type, align='WORLD', location=(0, 0, 0))
            new_light = bpy.context.active_object
            new_light.data.energy = preset.energy
            new_light.data.color = preset.color

        return {'FINISHED'}

def register():
    bpy.utils.register_class(OBJECT_PT_light_library)
    bpy.utils.register_class(OBJECT_OT_add_to_library)
    bpy.utils.register_class(OBJECT_OT_load_default_setups)
    bpy.utils.register_class(OBJECT_OT_remove_all_presets)
    bpy.utils.register_class(OBJECT_OT_add_preset_to_scene)
    bpy.utils.register_class(LightLibraryItem)
    bpy.types.Scene.light_library = bpy.props.CollectionProperty(type=LightLibraryItem)

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_light_library)
    bpy.utils.unregister_class(OBJECT_OT_add_to_library)
    bpy.utils.unregister_class(OBJECT_OT_load_default_setups)
    bpy.utils.unregister_class(OBJECT_OT_remove_all_presets)
    bpy.utils.unregister_class(OBJECT_OT_add_preset_to_scene)
    bpy.utils.unregister_class(LightLibraryItem)
    del bpy.types.Scene.light_library

class LightLibraryItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    energy: bpy.props.FloatProperty()
    color: bpy.props.FloatVectorProperty(size=3)
    light_type: bpy.props.StringProperty()

if __name__ == "__main__":
    register()
