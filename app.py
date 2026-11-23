from xml.dom import minidom

xmldoc = minidom.parse("spline6p.xml")

DOCUMENT = xmldoc.getElementsByTagName("noi:DOCUMENT")[0]
MODEL_SECTION = DOCUMENT.getElementsByTagName("noi:MODEL_SECTION")[0]
BASIS_LINE3D = MODEL_SECTION.getElementsByTagName("noi:BASIS_LINE3D")[0]
GEO_POLYHEDRON3D = BASIS_LINE3D.getElementsByTagName("noi:GEO_POLYHEDRON3D")[0]
GEO_POINT_LIST_3D = GEO_POLYHEDRON3D.getElementsByTagName("noi:GEO_POINT_LIST_3D")[0]
GEO_POINT = GEO_POINT_LIST_3D.getElementsByTagName("noi:GEO_POINT")

for GEO_POINT in  GEO_POINT_LIST_3D:
    print(x)