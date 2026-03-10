"""常见操作 → CATIA API 方法映射表。"""

COMMON_OPERATIONS = """\
# 常见操作 → CATIA API 映射表

| 用户描述 | VBScript 方法 | pycatia 方法 | 所属工厂 |
|---------|--------------|-------------|---------|
| 创建长方体/立方体 | 矩形草图 + AddNewPad | 矩形草图 + add_new_pad | ShapeFactory |
| 创建圆柱体 | 圆形草图 + AddNewPad | 圆形草图 + add_new_pad | ShapeFactory |
| 创建凹槽/口袋 | 草图 + AddNewPocket | 草图 + add_new_pocket | ShapeFactory |
| 打孔/钻孔 | AddNewHoleWith | add_new_hole_with | ShapeFactory |
| 倒圆角/R角 | AddNewEdgeFillet | add_new_edge_fillet | ShapeFactory |
| 倒角/C角 | AddNewChamfer | add_new_chamfer | ShapeFactory |
| 旋转体 | 草图 + AddNewShaft | 草图 + add_new_shaft | ShapeFactory |
| 旋转切除 | 草图 + AddNewGroove | 草图 + add_new_groove | ShapeFactory |
| 镜像 | AddNewMirror | add_new_mirror | ShapeFactory |
| 圆形阵列 | AddNewCircPattern | add_new_circ_pattern | ShapeFactory |
| 矩形阵列 | AddNewRectPattern | add_new_rect_pattern | ShapeFactory |
| 创建点 | AddNewPointCoord | add_new_point_coord | HybridShapeFactory |
| 创建线 | AddNewLinePtPt | add_new_line_pt_pt | HybridShapeFactory |
| 创建平面偏移 | AddNewPlaneOffset | add_new_plane_offset | HybridShapeFactory |
| 创建圆弧/圆 | AddNewCircleCtrRad | add_new_circle_ctr_rad | HybridShapeFactory |
| 扫掠 | AddNewSweepLine | add_new_sweep_line | HybridShapeFactory |
| 填充曲面 | AddNewFill | add_new_fill | HybridShapeFactory |
| 导出STEP | ExportData "stp" | export_data("stp") | Document |
| 导出IGES | ExportData "igs" | export_data("igs") | Document |
| 导出STL | ExportData "stl" | export_data("stl") | Document |
| 读取参数 | Parameters.Item(i) | parameters.item(i) | Part |
| 修改参数值 | Parameter.Value = x | parameter.value = x | Parameter |
| 添加公式 | Relations.CreateFormula | relations.create_formula | Relations |
| 添加设计表 | Relations.CreateDesignTable | relations.create_design_table | Relations |
| 测量距离 | SPAWorkbench.GetMeasurable | spa_workbench.get_measurable | SPAWorkbench |
| 选择对象 | Selection.SelectElement2 | selection.select_element2 | Selection |
| 隐藏/显示 | Selection.VisProperties | selection.vis_properties | Selection |
| 修改颜色 | VisPropertySet.SetRealColor | vis_property_set.set_real_color | VisProperties |

## 创建新文档
- VBScript: `CATIA.Documents.Add("Part")` / `CATIA.Documents.Add("Product")`
- pycatia: `caa.documents.add("Part")` / `caa.documents.add("Product")`

## 打开文档
- VBScript: `CATIA.Documents.Open("C:\\path\\to\\file.CATPart")`
- pycatia: `caa.documents.open(r"C:\\path\\to\\file.CATPart")`

## 保存文档
- VBScript: `oDoc.Save` 或 `oDoc.SaveAs "C:\\path\\to\\new.CATPart"`
- pycatia: `document.save()` 或 `document.save_as(r"C:\\path\\to\\new.CATPart")`
"""
