"""pycatia (Python) 代码模板和编码规范。"""

PYCATIA_TEMPLATES = """\
# pycatia Python 编码规范与模板

## 基本代码结构
```python
from pycatia import catia

# 连接 CATIA
caa = catia()

# 获取当前活动文档
document = caa.active_document
part_document = document  # 如果是 Part 文档

# 获取 Part 对象
part = part_document.part

# 获取主 Body
main_body = part.main_body

# 获取 ShapeFactory
shape_factory = part.shape_factory

# ... 你的代码 ...

# 更新零件
part.update()
```

## 模板：创建草图 + Pad（长方体）
```python
from pycatia import catia
from pycatia.mec_mod_interfaces.part import Part

caa = catia()
document = caa.active_document
part = document.part
main_body = part.main_body
shape_factory = part.shape_factory

# 获取 XY 平面
origin_elements = part.origin_elements
plane_xy = origin_elements.plane_xy
ref_plane = part.create_reference_from_object(plane_xy)

# 创建草图
sketches = main_body.sketches
sketch = sketches.add(ref_plane)

# 进入草图编辑
factory_2d = sketch.open_edition()

# 绘制矩形 50x30mm
line1 = factory_2d.create_line(0, 0, 50, 0)
line2 = factory_2d.create_line(50, 0, 50, 30)
line3 = factory_2d.create_line(50, 30, 0, 30)
line4 = factory_2d.create_line(0, 30, 0, 0)

# 关闭草图
sketch.close_edition()

# 创建 Pad（凸台）高度30mm
pad = shape_factory.add_new_pad(sketch, 30)

part.update()
print("长方体创建完成！")
```

## 模板：创建圆柱体
```python
from pycatia import catia

caa = catia()
document = caa.active_document
part = document.part
main_body = part.main_body
shape_factory = part.shape_factory

origin_elements = part.origin_elements
plane_xy = origin_elements.plane_xy
ref_plane = part.create_reference_from_object(plane_xy)

sketches = main_body.sketches
sketch = sketches.add(ref_plane)
factory_2d = sketch.open_edition()

# 创建圆（圆心0,0 半径30mm）
circle = factory_2d.create_closed_circle(0, 0, 30)

sketch.close_edition()

# 拉伸80mm
pad = shape_factory.add_new_pad(sketch, 80)
part.update()
print("圆柱体创建完成！")
```

## 模板：倒圆角
```python
# 获取 Pad 的引用
ref_pad = part.create_reference_from_object(pad)

# 创建倒圆角，半径5mm
fillet = shape_factory.add_new_edge_fillet_with_varying_radius(ref_pad, 1, 5)
# 或使用简化方法
# fillet = shape_factory.add_new_edge_fillet(ref_pad, catia_enum.CatFilletType.catTangencyFilletType, 5)

part.update()
```

## 模板：导出 STEP
```python
from pycatia import catia

caa = catia()
document = caa.active_document

export_path = r"C:\\output\\mypart.stp"
document.export_data(export_path, "stp")
print(f"已导出到: {export_path}")
```

## 模板：遍历参数导出 Excel
```python
from pycatia import catia
import csv

caa = catia()
document = caa.active_document
part = document.part
parameters = part.parameters

# 收集所有参数
param_list = []
for i in range(parameters.count):
    param = parameters.item(i + 1)  # 1-based index
    param_list.append({
        "name": param.name,
        "value": param.value_as_string()
    })

# 导出到 CSV
output_path = r"C:\\output\\parameters.csv"
with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "value"])
    writer.writeheader()
    writer.writerows(param_list)

print(f"已导出 {len(param_list)} 个参数到: {output_path}")
```

## 模板：创建孔
```python
from pycatia import catia

caa = catia()
document = caa.active_document
part = document.part
shape_factory = part.shape_factory

# 获取 Pad 顶面引用（通过 BRep 名称）
face_ref = part.create_reference_from_b_rep_name(
    "RSur:(Face:(Brp:(Pad.1;2);None:();Cf11:());WithTemporaryBody;WithoutBuildError;WithSelectingFeatureSupport;MFBRepVersion_CXR15)",
    part
)

# 创建孔：直径10mm，深度15mm
hole = shape_factory.add_new_hole_with(10, 15, face_ref)
part.update()
```

## 编码注意事项
1. pycatia 方法名使用 snake_case（对应 VBA 的 CamelCase）
2. 索引从 1 开始（与 VBA 一致，COM 约定）
3. 安装: `pip install pycatia`
4. 需要 CATIA V5 正在运行且有活动文档
5. 所有尺寸单位为毫米(mm)
"""
