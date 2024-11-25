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
from .. import consts
from ..funcs import (
    func_separate_shapekeys, 
    func_apply_as_shapekey, 
    func_apply_modifiers
)
from ..funcs.utils import func_object_utils


# シェイプキーをもつオブジェクトのモディファイアを適用
def apply_modifiers_with_shapekeys(self, remove_nonrender=True):
    source_obj = func_object_utils.get_active_object()
    print("apply_modifiers_with_shapekeys: [{0}] [{1}]".format(source_obj.name, source_obj.type))
    # Apply as shapekey用モディファイアのインデックスを検索
    apply_as_shape_index = -1
    apply_as_shape_modifier = None
    for i, modifier in enumerate(source_obj.modifiers):
        if modifier.name.startswith(consts.APPLY_AS_SHAPEKEY_PREFIX):
            apply_as_shape_index = i
            apply_as_shape_modifier = modifier
            print(f"apply as shape: {modifier.name}[{str(apply_as_shape_index)}]")
            break
    if apply_as_shape_index == 0:
        # Apply as shapekey用のモディファイアが一番上にあったらモディファイアをシェイプキーとして適用
        print("%AS% modifier is top")
        func_apply_as_shapekey.apply_as_shapekey(apply_as_shape_modifier)
        # 関数を再実行して終了
        print("re-execute apply_modifiers_with_shapekeys")
        apply_modifiers_with_shapekeys(self, remove_nonrender)
        return
    elif apply_as_shape_index >= 1:
        # 2番目以降にApply as shape用のモディファイアがあったら
        print("%AS% modifier is not top")
        # 一時オブジェクトを作成
        print("create tempobj")
        tempobj = func_object_utils.duplicate_object(source_obj)
        func_object_utils.deselect_all_objects()
        func_object_utils.select_object(tempobj, True)
        print("duplicate: " + tempobj.name)
        func_object_utils.set_active_object(source_obj)
        # モディファイアを一時オブジェクトにコピー
        print("copyto temp: make_links_data(type='MODIFIERS')")
        bpy.ops.object.make_links_data(type='MODIFIERS')

        # Apply as shapekeyとそれよりあとのモディファイアを削除
        for modifier in source_obj.modifiers[apply_as_shape_index:]:
            bpy.ops.object.modifier_remove(modifier=modifier.name)

        # 関数を再実行し、Apply as shapekeyより前のモディファイアを適用
        print("re-execute apply_modifiers_with_shapekeys (1)")
        apply_modifiers_with_shapekeys(self, remove_nonrender)

        # 削除していたモディファイアを一時オブジェクトから復元
        print("restore modifiers")
        func_object_utils.deselect_all_objects()
        func_object_utils.select_object(source_obj, True)
        func_object_utils.set_active_object(tempobj)
        print("restore: make_links_data(type='MODIFIERS')")
        bpy.ops.object.make_links_data(type='MODIFIERS')
        print("temp: " + str(tempobj))
        print("source: " + str(source_obj))
        func_object_utils.set_active_object(source_obj)
        # 適用済みのモディファイアを削除。これでモディファイアの1番目がApply as shapekey用のモディファイアになる
        for modifier in source_obj.modifiers[:apply_as_shape_index]:
            bpy.ops.object.modifier_remove(modifier=modifier.name)

        # 一時オブジェクトを削除
        print("remove tempobj")
        func_object_utils.remove_object(tempobj)
        func_object_utils.select_object(source_obj, True)
        func_object_utils.set_active_object(source_obj)

        # 関数を再実行して終了
        print("re-execute apply_modifiers_with_shapekeys (2)")
        apply_modifiers_with_shapekeys(self, remove_nonrender)
        return

    if source_obj.data.shape_keys and len(source_obj.data.shape_keys.key_blocks) == 1:
        # Basisしかなければシェイプキー削除
        print("remove basis: " + source_obj.name)
        # 0番目のシェイプキーをアクティブにする（これが無いとエラーが出る場合がある）
        source_obj.active_shape_key_index = 0
        bpy.ops.object.shape_key_remove(all=True)

    if source_obj.data.shape_keys is None or len(source_obj.data.shape_keys.key_blocks) == 0:
        # シェイプキーがなければモディファイア適用処理だけ実行
        print("only apply_modifiers: " + source_obj.name)
        func_apply_modifiers.apply_modifiers(remove_nonrender=remove_nonrender)
        return

    # 対象オブジェクトだけを選択
    func_object_utils.deselect_all_objects()
    func_object_utils.select_object(source_obj, True)
    func_object_utils.set_active_object(source_obj)

    # applymodifierの対象となるモディファイアがあるかどうか確認
    need_apply_modifier = False
    for modifier in source_obj.modifiers:
        if modifier.show_render or remove_nonrender:
            if modifier.name.startswith(consts.FORCE_APPLY_MODIFIER_PREFIX) or modifier.type != 'ARMATURE':
                need_apply_modifier = True
                break
    print(f"{source_obj.name}: Need Apply Modifiers: {str(need_apply_modifier)}")
    if need_apply_modifier:
        func_object_utils.select_object(source_obj, True)
        func_object_utils.set_active_object(source_obj)

        # シェイプキーの名前と数値を記憶
        active_shape_key_index = source_obj.active_shape_key_index
        shapekey_name_and_values = []
        for shapekey in source_obj.data.shape_keys.key_blocks:
            shapekey_name_and_values.append((shapekey.name, shapekey.value))

        # シェイプキーをそれぞれ別オブジェクトにしてモディファイア適用
        separated_objects = func_separate_shapekeys.separate_shapekeys(
            duplicate=False,
            enable_apply_modifiers=True,
            remove_nonrender=remove_nonrender,
            keep_original_shapekeys=False
        )

        print("Source: " + source_obj.name)
        print("------ Merge Separated Objects ------\n" + '\n'.join(
            [obj.name for obj in separated_objects]) + "\n----------------------------------")

        prev_obj_name = source_obj.name
        prev_vert_count = len(source_obj.data.vertices)

        shape_objects = []
        # オブジェクトを1つにまとめなおす
        func_object_utils.select_object(source_obj, True)
        func_object_utils.set_active_object(source_obj)
        for obj in separated_objects:
            # 前回のシェイプキーと頂点数が違ったら警告して処理を取り消し
            vert_count = len(obj.data.vertices)
            print("current: [{1}]({3})   prev: [{0}]({2})".format(prev_obj_name, obj.name, str(prev_vert_count),
                                                                  str(vert_count)))
            if vert_count != prev_vert_count:
                warn = bpy.app.translations.pgettext("mizore_error_apply_mod_with_shapekey_verts_count_difference").format(
                    obj_1 = prev_obj_name, 
                    obj_verts_1 = prev_vert_count,
                    obj_2 = obj.name, 
                    obj_verts_2 = vert_count
                    )
                print("!!!!! " + warn + "!!!!!")
                raise Exception(warn)

            prev_vert_count = vert_count
            prev_obj_name = obj.name

            # 一気にjoin_shapesするとシェイプキーの順番がおかしくなるので1つずつ
            # Armatureによる変形を無効化
            for modifier in obj.modifiers:
                if modifier.type == 'ARMATURE':
                    modifier.show_viewport = False
                    modifier.show_render = False
            func_object_utils.select_object(obj, True)
            print("Join: [{2}]({3}) -> [{0}]({1})".format(source_obj.name, str(len(source_obj.data.vertices)), obj.name,
                                                          str(vert_count)))
            bpy.ops.object.join_shapes()
            func_object_utils.select_object(obj, False)

            shape_objects.append(obj)
        func_object_utils.select_object(source_obj, False)
        # 使い終わったオブジェクトを削除
        func_object_utils.remove_objects(shape_objects)

        print(shapekey_name_and_values)
        print([v.name for v in source_obj.data.shape_keys.key_blocks])
        # シェイプキーの名前と数値を復元
        source_obj.active_shape_key_index = active_shape_key_index
        for i, shapekey in enumerate(source_obj.data.shape_keys.key_blocks):
            shapekey.name = shapekey_name_and_values[i][0]
            shapekey.value = shapekey_name_and_values[i][1]

    print("Shapekey Count (Include Basis Shapekey): " + str(len(source_obj.data.shape_keys.key_blocks)))

    func_object_utils.select_object(source_obj, True)
    func_object_utils.set_active_object(source_obj)
