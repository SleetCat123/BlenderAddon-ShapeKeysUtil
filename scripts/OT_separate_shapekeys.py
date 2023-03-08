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
from bpy.props import BoolProperty
from . import func_utils, func_separate_shapekeys


class OBJECT_OT_specials_shapekeys_util_separateobj(bpy.types.Operator):
    bl_idname = "object.shapekeys_util_separateobj"
    bl_label = "Separate Objects"
    bl_description = bpy.app.translations.pgettext(bl_idname + "_desc")
    bl_options = {'REGISTER', 'UNDO'}

    duplicate: BoolProperty(name="Duplicate", default=False,
                            description=bpy.app.translations.pgettext(bl_idname + "_duplicate"))
    apply_modifiers: BoolProperty(name="Apply Modifiers", default=False,
                                  description=bpy.app.translations.pgettext(bl_idname + "_apply_modifiers"))
    remove_nonrender: BoolProperty(name="Remove NonRender", default=True,
                                   description=bpy.app.translations.pgettext("remove_nonrender"))

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj.type == 'MESH'

    def execute(self, context):
        source_obj = context.object

        # 実行する必要がなければキャンセル
        if source_obj.data.shape_keys is None or len(source_obj.data.shape_keys.key_blocks) == 0:
            return {'CANCELLED'}

        func_utils.deselect_all_objects()
        func_utils.select_object(source_obj, True)
        func_utils.set_active_object(source_obj)

        # シェイプキーをそれぞれ別オブジェクトにする
        func_separate_shapekeys.separate_shapekeys(self.duplicate, self.apply_modifiers, self.remove_nonrender)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_OT_specials_shapekeys_util_separateobj)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_specials_shapekeys_util_separateobj)