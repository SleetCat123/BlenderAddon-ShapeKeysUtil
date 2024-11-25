# ##### BEGIN GPL LICENSE BLOCK #####
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
from ..funcs.func_apply_modifiers_with_shapekeys import apply_modifiers_with_shapekeys
from ..funcs.func_separate_lr_shapekey_all import separate_lr_shapekey_all


# MizoresCustomExporter連携用
class OBJECT_OT_apply_modifiers_for_mizores_custom_exporter_addon(bpy.types.Operator):
    bl_idname = "object.shapekeys_util_apply_mod_for_exporter_addon"
    bl_label = "[Internal] Apply Modifiers With Shapekeys For MizoresCustomExporter Addon"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print("ShapekeysUtil - Apply Modifiers With Shapekeys")
        apply_modifiers_with_shapekeys(self=self, remove_nonrender=False)
        return {'FINISHED'}


class OBJECT_OT_separate_lr_shapekey_for_mizores_custom_exporter_addon(bpy.types.Operator):
    bl_idname = "object.shapekeys_util_separate_lr_shapekey_for_exporter"
    bl_label = "[Internal] Separate All Shape Key Left and Right For MizoresCustomExporter Addon"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print("ShapekeysUtil - Separate LR Shapekeys")
        separate_lr_shapekey_all(duplicate=False, enable_sort=False, auto_detect=True)
        return {'FINISHED'}


classes = [
    OBJECT_OT_apply_modifiers_for_mizores_custom_exporter_addon,
    OBJECT_OT_separate_lr_shapekey_for_mizores_custom_exporter_addon,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

