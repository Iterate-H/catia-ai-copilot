"""CATIA V5 对象模型参考 — 核心类层次与常用属性/方法。"""

CATIA_API_REFERENCE = """\
# CATIA V5 Automation 对象模型参考

## 核心对象层次
```
Application (CATIA)
├── ActiveDocument → Document
│   ├── Part → Part
│   │   ├── Bodies → Bodies → Body (零件几何集合)
│   │   │   └── Shapes → Shapes → Shape
│   │   ├── HybridBodies → HybridBodies → HybridBody (几何图形集)
│   │   ├── Parameters → Parameters → Parameter
│   │   ├── Relations → Relations → Relation
│   │   └── ShapeFactory / HybridShapeFactory
│   ├── Product → Product
│   │   ├── Products → Products → Product (子组件)
│   │   └── Parameters → Parameters
│   └── Selection → Selection
├── Documents → Documents
└── SystemService → SystemService
```

## Part Design 核心对象
- **Body**: 零件实体，包含一系列有序的特征(Shape)
- **Sketch**: 草图，2D几何的容器
  - OpenEdition() → 进入编辑模式
  - CloseEdition() → 退出编辑模式
  - Factory2D → 获取2D工厂对象
- **Factory2D**: 草图中的2D几何创建工厂
  - CreateClosedCircle(x, y, r) → Circle2D
  - CreateLine(x1, y1, x2, y2) → Line2D
  - CreatePoint(x, y) → Point2D
- **ShapeFactory**: 3D特征创建工厂
  - AddNewPad(sketch, height) → Pad
  - AddNewPocket(sketch, depth) → Pocket
  - AddNewShaft(sketch, angle) → Shaft
  - AddNewGroove(sketch, angle) → Groove
  - AddNewHole(face, depth) → Hole
  - AddNewEdgeFillet(radius) → EdgeFillet
  - AddNewChamfer(length, angle) → Chamfer
  - AddNewCircPattern(shape, n, angle) → CircPattern
  - AddNewRectPattern(shape, n1, n2, step1, step2) → RectPattern
  - AddNewMirror(plane) → Mirror
- **Pad**: 凸台特征
  - FirstLimit.Dimension.Value = height
  - DirectionOrientation = catRegular / catReverse
- **Pocket**: 凹槽（减材料）
  - FirstLimit.Dimension.Value = depth
- **Hole**: 孔特征
  - Diameter.Value, Depth.Value, Type (Simple/Counterbored/Tapered)
- **EdgeFillet**: 倒圆角
  - Radius.Value
- **Chamfer**: 倒角
  - Length1, Angle

## Generative Shape Design (GSD) 核心对象
- **HybridShapeFactory**: 曲面/线框创建工厂
  - AddNewPointCoord(x, y, z) → HybridShapePointCoord
  - AddNewLinePtPt(pt1, pt2) → HybridShapeLinePtPt
  - AddNewPlaneOffsetPt(plane, pt, offset) → HybridShapePlaneOffset
  - AddNewCircleCtrRad(center, support, radius) → HybridShapeCircleCtrRad
  - AddNewExtremum(shape, dir, min/max) → HybridShapeExtremum
  - AddNewSweepLine(guide) → HybridShapeSweepLine
  - AddNewFill() → HybridShapeFill
  - AddNewJoin(curve1, curve2) → HybridShapeAssemble

## Reference 获取方式
- part.CreateReferenceFromObject(geometryObject) → Reference
- part.OriginElements.PlaneXY / PlaneYZ / PlaneZX → Reference
- body.Shapes.Item(n) → Shape → 可创建 Reference

## 重要枚举值
- catRegular / catReverse → 方向
- catSimpleHole / catCounterbored / catTapered → 孔类型
- catStartLimit / catUpToLast / catUpToSurface → 限制类型

## 更新零件
- part.Update() → 重新计算所有特征
- part.UpdateObject(shape) → 只更新指定特征
"""
