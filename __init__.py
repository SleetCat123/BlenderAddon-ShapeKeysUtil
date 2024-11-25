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
from .scripts.funcs.utils import func_package_utils


bl_info = {
    "name": "ShapeKeys Util",
    "author": "@sleetcat123(Twitter)",
    "version": (2, 1, 0),
    "blender": (2, 80, 0),
    "location": "",
    "description": "",
    "category": "Object"
}

if 'bpy' in locals():
    from importlib import reload
    import sys
    for k, v in list(sys.modules.items()):
        if k.startswith(func_package_utils.get_package_root()):
            reload(v)
else:
    from .scripts import (
        addon_preferences,
        translations,
    )
    from .scripts.link import (
        link_with_AutoMerge,
        link_with_MizoresCustomExporter
    )
    from .scripts.menu import (
        menu_edit_mesh_context,
        menu_object_context
    )
    from .scripts.ops import (
        op_apply_modifiers,
        op_apply_selected_modifiers,
        op_assign_lr_shapekey_tag,
        op_copy_shapekey_to_others,
        op_separate_lr_shapekey,
        op_separate_lr_shapekey_all,
        op_separate_lr_shapekey_all_tag_detect,
        op_separate_shapekeys,
        op_sideofactive_point,
    )

import bpy


classes = [
    addon_preferences,
    translations,
    
    link_with_AutoMerge,
    link_with_MizoresCustomExporter,

    menu_edit_mesh_context,
    menu_object_context,

    op_apply_modifiers,
    op_apply_selected_modifiers,
    op_assign_lr_shapekey_tag,
    op_copy_shapekey_to_others,
    op_separate_lr_shapekey,
    op_separate_lr_shapekey_all,
    op_separate_lr_shapekey_all_tag_detect,
    op_separate_shapekeys,
    op_sideofactive_point,
]


def register():
    for cls in classes:
        try:
            getattr(cls, "register", None)()
        except Exception as e:
            print(f"Error registering {cls.__name__}")
            print(e)


def unregister():
    for cls in classes:
        try:
            getattr(cls, "unregister", None)()
        except Exception as e:
            print(f"Error unregistering {cls.__name__}")
            print(e)


if __name__ == "__main__":
    register()
