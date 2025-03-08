# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 17:54:13 2025

@author: brand
"""

bl_info = {
    "name": "Animation Editor GUI",
    "blender": (2, 80, 0),
    "category": "Animation",
    "description": "Edit animation keyframes in a user-friendly GUI.",
    "author": "Your Name",
    "version": (1, 0, 0),
}

import bpy

class ANIM_EDITOR_PT_Panel(bpy.types.Panel):
    """Creates a panel in the N-panel for animation editing."""
    bl_label = "Animation Editor"
    bl_idname = "ANIM_EDITOR_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Animation'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.label(text="Edit Animation Keyframes")
        
        layout.prop(scene, "anim_edit_start")
        layout.prop(scene, "anim_edit_end")
        layout.prop(scene, "anim_edit_axis", text="Axis")
        layout.prop(scene, "anim_edit_mode", text="Mode")
        layout.prop(scene, "anim_edit_value", text="Adjust By")
        
        layout.operator("anim.edit_keyframes", text="Apply Changes")

class ANIM_OT_EditKeyframes(bpy.types.Operator):
    """Operator to edit animation keyframes based on user input."""
    bl_idname = "anim.edit_keyframes"
    bl_label = "Edit Keyframes"
    
    def execute(self, context):
        obj = context.object
        scene = context.scene
        start_frame = scene.anim_edit_start
        end_frame = scene.anim_edit_end
        axis_index = {"X": 0, "Y": 1, "Z": 2}[scene.anim_edit_axis]
        mode = scene.anim_edit_mode
        adjust_value = scene.anim_edit_value
        
        if obj and obj.animation_data and obj.animation_data.action:
            action = obj.animation_data.action
            
            for fcurve in action.fcurves:
                if mode.lower() in fcurve.data_path and fcurve.array_index == axis_index:
                    for keyframe in fcurve.keyframe_points:
                        if start_frame <= keyframe.co[0] <= end_frame:
                            keyframe.co[1] += adjust_value
            
            bpy.context.view_layer.update()
            self.report({'INFO'}, "Animation keyframes updated successfully!")
        else:
            self.report({'WARNING'}, "No animation data found!")
        
        return {'FINISHED'}

# Register properties
classes = [ANIM_EDITOR_PT_Panel, ANIM_OT_EditKeyframes]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.anim_edit_start = bpy.props.IntProperty(name="From Frame", default=1)
    bpy.types.Scene.anim_edit_end = bpy.props.IntProperty(name="To Frame", default=250)
    bpy.types.Scene.anim_edit_axis = bpy.props.EnumProperty(
        name="Axis", items=[("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", "")])
    bpy.types.Scene.anim_edit_mode = bpy.props.EnumProperty(
        name="Mode", items=[("location", "Move", ""), ("rotation", "Rotate", ""), ("scale", "Scale", "")])
    bpy.types.Scene.anim_edit_value = bpy.props.FloatProperty(name="Adjust By", default=1.0)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.anim_edit_start
    del bpy.types.Scene.anim_edit_end
    del bpy.types.Scene.anim_edit_axis
    del bpy.types.Scene.anim_edit_mode
    del bpy.types.Scene.anim_edit_value

if __name__ == "__main__":
    register()
