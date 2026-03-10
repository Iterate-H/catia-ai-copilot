"""VBScript (CATScript) 代码模板和编码规范。"""

VBA_TEMPLATES = """\
# VBScript / CATScript 编码规范与模板

## 基本代码结构（CATMain 入口）
```vbscript
Sub CATMain()
    ' 获取 CATIA 应用程序对象
    Dim CATIA As Object
    Set CATIA = GetObject(, "CATIA.Application")

    ' 获取当前活动文档
    Dim oDoc As Document
    Set oDoc = CATIA.ActiveDocument

    ' 获取 Part 对象
    Dim oPart As Part
    Set oPart = oDoc.Part

    ' 获取主 Body
    Dim oBody As Body
    Set oBody = oPart.MainBody

    ' 获取 ShapeFactory
    Dim oFactory As ShapeFactory
    Set oFactory = oPart.ShapeFactory

    ' ... 你的代码 ...

    ' 更新零件
    oPart.Update
End Sub
```

## 模板：创建草图 + Pad
```vbscript
' === 创建草图 ===
Dim oSketches As Sketches
Set oSketches = oBody.Sketches

' 在 XY 平面上创建草图
Dim oRefPlane As Reference
Set oRefPlane = oPart.OriginElements.PlaneXY

Dim oSketch As Sketch
Set oSketch = oSketches.Add(oRefPlane)

' 进入草图编辑模式
Dim oFactory2D As Factory2D
Set oFactory2D = oSketch.OpenEdition()

' 创建矩形（4条线）
Dim oLine1 As Line2D
Set oLine1 = oFactory2D.CreateLine(0, 0, 50, 0)
Dim oLine2 As Line2D
Set oLine2 = oFactory2D.CreateLine(50, 0, 50, 30)
Dim oLine3 As Line2D
Set oLine3 = oFactory2D.CreateLine(50, 30, 0, 30)
Dim oLine4 As Line2D
Set oLine4 = oFactory2D.CreateLine(0, 30, 0, 0)

' 关闭草图编辑
oSketch.CloseEdition

' === 创建 Pad ===
Dim oPad As Pad
Set oPad = oFactory.AddNewPad(oSketch, 30)

oPart.Update
```

## 模板：创建圆形草图 + Pad（圆柱体）
```vbscript
Dim oSketch As Sketch
Set oSketch = oBody.Sketches.Add(oPart.OriginElements.PlaneXY)

Dim oFactory2D As Factory2D
Set oFactory2D = oSketch.OpenEdition()

' 创建圆（圆心x, 圆心y, 半径）
Dim oCircle As Circle2D
Set oCircle = oFactory2D.CreateClosedCircle(0, 0, 30)

oSketch.CloseEdition

Dim oPad As Pad
Set oPad = oFactory.AddNewPad(oSketch, 80)
oPart.Update
```

## 模板：在面上打孔
```vbscript
' 选择面（通常通过名称或交互选择）
Dim oRef As Reference
Set oRef = oPart.CreateReferenceFromBRepName("RSur:(Face:(Brp:(Pad.1;2);None:();Cf11:());WithTemporaryBody;WithoutBuildError;WithSelectingFeatureSupport;MFBRepVersion_CXR15)", oPart)

' 或使用 Selection 交互选择
' CATIA.ActiveDocument.Selection.SelectElement2(Array("Face"), "请选择孔的放置面", False)

Dim oHole As Hole
Set oHole = oFactory.AddNewHoleWith(10, 15, oRef)
' 10 = 直径, 15 = 深度
oPart.Update
```

## 模板：倒圆角
```vbscript
' 获取需要倒角的边
Dim oEdgeRef As Reference
Set oEdgeRef = oPart.CreateReferenceFromObject(oPad)

Dim oFillet As EdgeFillet
Set oFillet = oFactory.AddNewEdgeFillet(oEdgeRef, catTangencyFilletType, 5)
' 5 = 圆角半径
oPart.Update
```

## 模板：圆形阵列
```vbscript
Dim oRefAxis As Reference
Set oRefAxis = oPart.OriginElements.PlaneZX  ' 旋转轴参考

Dim oCircPattern As CircPattern
Set oCircPattern = oFactory.AddNewCircPattern(oHole, 1, 10, 0, 36, 1, 1, oRefAxis, oRefAxis, True, 0, True)
' 参数: 形状, 径向数量, 角向数量, 径向间距, 角度间距, ...
oPart.Update
```

## 模板：导出 STEP
```vbscript
Dim sFilePath As String
sFilePath = "C:\\output\\mypart.stp"

oDoc.ExportData sFilePath, "stp"
```

## 模板：遍历参数并导出 Excel
```vbscript
Dim oParams As Parameters
Set oParams = oPart.Parameters

Dim oExcel As Object
Set oExcel = CreateObject("Excel.Application")
oExcel.Visible = True

Dim oWB As Object
Set oWB = oExcel.Workbooks.Add()
Dim oWS As Object
Set oWS = oWB.Worksheets(1)

oWS.Cells(1, 1).Value = "参数名"
oWS.Cells(1, 2).Value = "值"

Dim i As Integer
For i = 1 To oParams.Count
    oWS.Cells(i + 1, 1).Value = oParams.Item(i).Name
    oWS.Cells(i + 1, 2).Value = oParams.Item(i).ValueAsString
Next
```

## 编码注意事项
1. 所有尺寸单位为毫米(mm)，角度为度(°)
2. 使用 `Set` 关键字赋值对象引用
3. `Dim ... As Object` 比强类型声明兼容性更好
4. 必须调用 `oPart.Update` 来刷新特征树
5. 草图操作必须在 OpenEdition/CloseEdition 之间
"""
