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
from . import func_utils, consts, func_apply_modifiers, func_apply_as_shapekey, func_separate_shapekeys


# シェイプキーをもつオブジェクトのモディファイアを適用
def apply_modifiers_with_shapekeys(self, source_obj, duplicate, remove_nonrender=True):
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
        # Apply as shapekey用のモディファイアが一番上にあったらApply as shapekeyを実行
        print("apply_as_shapekey__B1")
        func_apply_as_shapekey.apply_as_shapekey(apply_as_shape_modifier)
        print("apply_as_shapekey__B2")
        # 関数を再実行して終了
        return apply_modifiers_with_shapekeys(self, source_obj, duplicate, remove_nonrender)
    elif apply_as_shape_index != -1:
        # 2番目以降にApply as shape用のモディファイアがあったら
        # 一時オブジェクトを作成
        bpy.ops.object.duplicate()
        tempobj = func_utils.get_active_object()
        func_utils.select_object(tempobj, True)
        print("duplicate: " + tempobj.name)
        func_utils.set_active_object(source_obj)
        # モディファイアを一時オブジェクトにコピー
        print("copyto temp: make_links_data(type='MODIFIERS')")
        bpy.ops.object.make_links_data(type='MODIFIERS')

        # Apply as shapekeyとそれよりあとのモディファイアを削除
        for modifier in source_obj.modifiers[apply_as_shape_index:]:
            bpy.ops.object.modifier_remove(modifier=modifier.name)

        # 関数を再実行
        success = apply_modifiers_with_shapekeys(self, source_obj, duplicate, remove_nonrender)
        if not success:
            # 処理に失敗したら処理前のデータを復元して終了
            func_utils.select_object(source_obj, True)
            func_utils.set_active_object(tempobj)
            bpy.ops.object.make_links_data(type='OBDATA')
            bpy.ops.object.make_links_data(type='MODIFIERS')
            return False

        # 削除していたモディファイアを一時オブジェクトから復元
        func_utils.select_object(source_obj, True)
        func_utils.set_active_object(tempobj)
        print("restore: make_links_data(type='MODIFIERS')")
        bpy.ops.object.make_links_data(type='MODIFIERS')
        print("a")
        func_utils.set_active_object(source_obj)
        # 適用済みのモディファイアを削除
        for modifier in source_obj.modifiers[:apply_as_shape_index]:
            bpy.ops.object.modifier_remove(modifier=modifier.name)

        # 一時オブジェクトを削除
        func_utils.select_object(source_obj, False)
        func_utils.select_object(tempobj, True)
        func_utils.remove_objects()
        func_utils.select_object(source_obj, True)
        func_utils.set_active_object(source_obj)

        # 関数を再実行して終了
        return apply_modifiers_with_shapekeys(self, source_obj, duplicate, remove_nonrender)

    if source_obj.data.shape_keys and len(source_obj.data.shape_keys.key_blocks) == 1:
        # Basisしかなければシェイプキー削除
        print("remove basis: " + source_obj.name)
        bpy.ops.object.shape_key_remove(all=True)

    if source_obj.data.shape_keys is None or len(source_obj.data.shape_keys.key_blocks) == 0:
        # シェイプキーがなければモディファイア適用処理だけ実行
        print("only apply_modifiers: " + source_obj.name)
        func_apply_modifiers.apply_modifiers(remove_nonrender=remove_nonrender)
        if duplicate:
            bpy.ops.object.duplicate()
        return True

    # 対象オブジェクトだけを選択
    func_utils.deselect_all_objects()
    func_utils.select_object(source_obj, True)
    func_utils.set_active_object(source_obj)

    # applymodifierの対象となるモディファイアがあるかどうか確認
    need_apply_modifier = False
    for modifier in source_obj.modifiers:
        if modifier.show_render or remove_nonrender:
            if modifier.name.startswith(consts.APPLY_AS_SHAPEKEY_PREFIX) or (
                    modifier.name.startswith(consts.FORCE_APPLY_MODIFIER_PREFIX) or modifier.type != 'ARMATURE'):
                need_apply_modifier = True
                break
    print("{0}: Need Apply Modifiers: {1}".format(source_obj.name, str(need_apply_modifier)))
    if need_apply_modifier:
        # オブジェクトを複製
        bpy.ops.object.duplicate()
        source_obj_dup = func_utils.get_active_object()
        func_utils.select_object(source_obj_dup, False)
        func_utils.select_object(source_obj, True)
        func_utils.set_active_object(source_obj)

        # シェイプキーの名前と数値を記憶
        active_shape_key_index = source_obj.active_shape_key_index
        shapekey_name_and_values = []
        for shapekey in source_obj.data.shape_keys.key_blocks:
            shapekey_name_and_values.append((shapekey.name, shapekey.value))

        # シェイプキーをそれぞれ別オブジェクトにしてモディファイア適用
        separated_objects = func_separate_shapekeys.separate_shapekeys(duplicate=False, enable_apply_modifiers=True,
                                               remove_nonrender=remove_nonrender)

        print("Source: " + source_obj.name)
        print("------ Merge Separated Objects ------\n" + '\n'.join(
            [obj.name for obj in separated_objects]) + "\n----------------------------------")

        prev_obj_name = source_obj.name
        prev_vert_count = len(source_obj.data.vertices)

        shape_objects = []
        # オブジェクトを1つにまとめなおす
        func_utils.select_object(source_obj, True)
        func_utils.set_active_object(source_obj)
        for obj in separated_objects:
            # 前回のシェイプキーと頂点数が違ったら警告して処理を取り消し
            vert_count = len(obj.data.vertices)
            print("current: [{1}]({3})   prev: [{0}]({2})".format(prev_obj_name, obj.name, str(prev_vert_count),
                                                                  str(vert_count)))
            if vert_count != prev_vert_count:
                warn = bpy.app.translations.pgettext("verts_count_difference").format(prev_obj_name, obj.name,
                                                                                      prev_vert_count, vert_count)
                if self: self.report({'ERROR'}, warn)
                print("!!!!! " + warn + "!!!!!")
                # 処理中オブジェクトを削除
                func_utils.select_object(source_obj, True)
                for child in source_obj.children:
                    func_utils.select_object(child, True)
                func_utils.remove_objects()
                func_utils.select_object(source_obj_dup, True)
                func_utils.set_active_object(source_obj_dup)
                return False

            prev_vert_count = vert_count
            prev_obj_name = obj.name

            # 一気にjoin_shapesするとシェイプキーの順番がおかしくなるので1つずつ
            func_utils.select_object(obj, True)
            print("Join: [{2}]({3}) -> [{0}]({1})".format(source_obj.name, str(len(source_obj.data.vertices)), obj.name,
                                                          str(vert_count)))
            bpy.ops.object.join_shapes()
            func_utils.select_object(obj, False)

            shape_objects.append(obj)
        func_utils.select_object(source_obj, False)
        # 使い終わったオブジェクトを削除
        func_utils.select_objects(shape_objects, True)
        func_utils.remove_objects()

        # シェイプキーの名前と数値を復元
        source_obj.active_shape_key_index = active_shape_key_index
        for i, shapekey in enumerate(source_obj.data.shape_keys.key_blocks):
            shapekey.name = shapekey_name_and_values[i][0]
            shapekey.value = shapekey_name_and_values[i][1]

        if not duplicate:
            # 処理が正常に終了したら複製オブジェクトを削除する
            func_utils.select_object(source_obj_dup, True)
            func_utils.remove_objects()

    print("Shapekey Count (Include Basis Shapekey): " + str(len(source_obj.data.shape_keys.key_blocks)))

    func_utils.select_object(source_obj, True)
    func_utils.set_active_object(source_obj)
    return True