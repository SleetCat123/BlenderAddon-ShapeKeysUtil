
## ◆更新履歴

### 2024-11-25 v2.1.0
- add: 名前が%AS%で終わるSurfaceDeformモディファイアのターゲットオブジェクトにシェイプキーが2つ以上存在していて、最初のシェイプキーの名前が"All"ならターゲットオブジェクトのシェイプキーによる変形結果を個別にシェイプキーとして適用するように
- change: シェイプキーがある場合、SurfaceDeformモディファイアはBasisシェイプに対して適用されるように
- remove: ShapeKeys Util → Apply ModifiersのDuplicateチェックボックスを廃止

### 2024-09-11 v2.0.2
- fix: アドオン連携機能の実行時にエラーが出る不具合を修正
---
### 2024-09-07 v2.0.1
- add: 一部の処理の失敗時に実行前の状態を自動で復元するようにした（自動でUndoを実行）
- fix: リンクされたオブジェクトのモディファイア適用が正常に行われない不具合を修正

### 2024-09-03 v2.0.0
- add: %AS%接頭辞によるモディファイアのApply as shapeで、すでに同名のシェイプキーが存在する場合はそのシェイプキーの形状に対してモディファイアの変形を適用するようにした
- add: %AS%接頭辞によるモディファイアのApply as shapeのとき、$以降の文字列を無視するようにした
- add: Blender内での機能説明文を一部追加
- add: アクティブなモディファイアのみを適用するオペレーターを追加
- add:　アクティブオブジェクトの形状をシェイプキーとして他のオブジェクトに追加するオペレーターを追加
- fix: x=0付近に頂点が無いメッシュに対してSeparate Shape Key Left and Rightを実行するとエラーが出ることがあったのを修正
- change: **スクリプトを複数ファイルに分離。不具合回避のため、バージョンアップ時には古いバージョンを削除してから導入してください。**
- change: Select Side of Active from PointのThresholdに負の値を設定できるように変更
- change: シェイプキー分割の内部処理を変更
- change: テキスト翻訳の内部処理を変更
  - [MizoresCustomExporter](https://github.com/SleetCat123/BlenderAddon_MizoresCustomExporter): 1.0.0-
  - [AutoMerge](https://github.com/SleetCat123/BlenderAddon-AutoMerge): 3.0.0-
---
### 2022-12-11　Ver_1.1.6
- change: 右クリック→ShapeKeys Util→Apply Modifiers が選択中のオブジェクト全てに適用されるように（いままではアクティブオブジェクトだけに適用されていた）
- fix: 適用対象となるモディファイアが無いオブジェクトに対してApply Modifiersを使用するとエラーが出る不具合を修正。
- fix: ApplyModifiers実行時、Basisシェイプキーと1番目のシェイプキーの頂点数が異なっていた場合に意図しないエラーが出てしまう不具合を修正。
- fix: シェイプキーがBasisしかない状態でApply Modifiersを使うとエラーが出る不具合を修正。
- fix: 複数インスタンス化されているオブジェクトのモディファイア適用が正常に行われない不具合を修正。
---
### 2022-02-15　Ver_1.1.5
- fix: （3.0以降？）Separate Shape Key Left and Rightが動作していなかった不具合を修正。
- change: Blender 2.7系への互換性確保コードを削除。
- change: テキスト表示言語切り替えの実装方法を変更。
---
### 2021-11-30　Ver_1.1.4
- change: モディファイア適用時、名前が%AS%から始まるモディファイアをシェイプキーとして適用（Apply as shapekey）するようにした（シェイプキー適用時に名前の%AS%は削除）
- change: モディファイア適用時、無効なモディファイア（対象オブジェクトが指定されていないなどの状態）を削除するようにした（無効なモディファイアがあるとシェイプキーがエクスポートされなくなる現象対策）
---
### 2021-06-15　Ver_1.1.3
- fix: Editモードで選択モードが頂点以外になっているとき、Separate Shape Key Left and Rightなどの機能が正常に動作しない不具合を修正。
- fix: Blender 2.93で一部機能が正常に動作しない不具合を修正。
---
### 2020-02-24　Ver_1.1.2
- change: Apply Modifier時、レンダリングが無効化されたモディファイア（モディファイア一覧でカメラアイコンが押されていないもの）を削除せずそのまま残すことができるように。
- change: Apply Modifierの対象外モディファイア（現在はArmatureのみ）であっても、モディファイアの名前欄の先頭に文字列“%A%”を付けることで強制的にモディファイアを適用させることができるように。
- change: Apply Modifier時に頂点数が一致しないシェイプキーがある場合、警告を表示して処理を取り消すように。
- change: Separate Objectsで生成されたオブジェクトを元オブジェクトの子に設定するようにした。
- fix: Apply Modifier時、無効なモディファイア（対象オブジェクトが指定されていないなどの状態）があるとエラーが出る不具合を修正。
- fix: Editモードで非表示になっている頂点がある状態でSeparate Shape Key Left and Right系統の機能を使うと正常に動作しないことがある不具合を修正
- change: Addon Preferenceで、一部処理に挟まれる待機処理の間隔（Wait Interval）と長さ（Wait Sleep）を設定できるように。
- change: Blender2.8系の対応が不完全だったのを修正。
---
### 2019-02-11　Ver_1.0.0
- 公開