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
import traceback
from bpy.props import BoolProperty
from ..funcs import func_apply_modifiers_with_shapekeys
from ..funcs.utils import func_object_utils


class OBJECT_OT_specials_shapekeys_util_apply_modifiers(bpy.types.Operator):
    bl_idname = "object.shapekeys_util_apply_modifiers"
    bl_label = "Apply Modifiers"
    bl_description = "Apply all modifiers except for Armature.\nCan use even if has a shape key.\nWarning: It may take a while"
    bl_options = {'REGISTER', 'UNDO'}

    remove_nonrender: BoolProperty(
        name="Remove NonRender",
        default=True,
        description="A non-render modifier will be removed."
    )

    def execute(self, context):
        try:
            active = func_object_utils.get_active_object()
            selected_objects = bpy.context.selected_objects
            targets = [d for d in selected_objects if d.type == 'MESH']
            if active.type == 'MESH' and active not in targets:
                targets.append(active)

            func_object_utils.deselect_all_objects()
            func_object_utils.select_objects(targets, True)
            # リンクされたオブジェクトのモディファイアは適用できないので予めリンクを解除しておく
            bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=True, obdata=True, material=False, animation=False)

            for obj in targets:
                func_object_utils.set_active_object(obj)
                func_apply_modifiers_with_shapekeys.apply_modifiers_with_shapekeys(remove_nonrender=self.remove_nonrender)
            func_object_utils.select_objects(selected_objects, True)
            func_object_utils.set_active_object(active)
            return {'FINISHED'}
        except Exception as e:
            bpy.ops.ed.undo_push(message = "Restore point")
            bpy.ops.ed.undo()
            bpy.ops.ed.undo_push(message = "Restore point")
            traceback.print_exc()
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}


translations_dict = {
    "ja_JP": {
        ("*", "Apply all modifiers except for Armature.\nCan use even if has a shape key.\nWarning: It may take a while"):
            "Armature以外の全モディファイアを適用します。\nシェイプキーがあっても使用できます。\n注意：少し時間がかかります",
        ("*", "Duplicate"): "複製",
        ("*", "Execute the function on the copied object"): "対象オブジェクトのコピーに対して処理を行います",
        ("*", "Remove NonRender"): "レンダリング無効は削除",
        ("*", "A non-render modifier will be removed."):
            "レンダリング無効化状態のモディファイア\n（モディファイア一覧でカメラアイコンが押されていない）\nを削除します。",
    },
}


def register():
    bpy.utils.register_class(OBJECT_OT_specials_shapekeys_util_apply_modifiers)
    bpy.app.translations.register(__name__, translations_dict)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_specials_shapekeys_util_apply_modifiers)
    bpy.app.translations.unregister(__name__)

