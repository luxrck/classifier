import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1

import QtMultimedia 5.4

import Material 0.1
import Material.ListItems 0.1 as ListItem
import Material.Extras 0.1

Dialog {

    id: imgclipdialog

    property alias imgsource: imgpreview.source

    signal imageClipped(var preview, var cliparea)

    //title: "Please select face area from this image"

    positiveButtonText: "Next"
    positiveButton.enabled: false
    negativeButton.visible: false

    interactive: false

    onAccepted: {
        imgclipdialog.close()

        var isw = imgpreview.sourceSize.width
        var ish = imgpreview.sourceSize.height

        var sx = isw / imgpreview.width
        var sy = ish / imgpreview.height

        var x = imgcliprect.x * sx
        var y = imgcliprect.y * sy
        var width = imgcliprect.width * sx
        var height = imgcliprect.height * sy

        console.log("x:"+x+","+y+","+width+","+height)

        imgcliprect.width = 0
        imgcliprect.height = 0

        return imageClipped(imgsource, {"x": x, "y": y, "width": width, "height": height})
    }

    dialogContent: [
        Image {
            id: imgpreview

            anchors {
                left: parent.left
                right: parent.right
            }

            height: imgpreview.width * 0.75

            Rectangle {
                id: imgcliprect

                property var x0: 0
                property var y0: 0

                color: Qt.rgba(0, 0, 0, 0.5)
            }

            DropArea { id: imgdroparea; anchors.fill: parent }

            MouseArea {
                id: imgmousearea

                anchors.fill: parent

                onPressed: {
                    imgcliprect.x = mouse.x
                    imgcliprect.y = mouse.y
                    imgcliprect.x0 = mouse.x
                    imgcliprect.y0 = mouse.y
                    imgcliprect.width = imgcliprect.height = 0
                }

                onPositionChanged: {
                    if (imgmousearea.pressed) {
                        var x0 = Math.min(mouse.x, imgcliprect.x0)
                        var y0 = Math.min(mouse.y, imgcliprect.y0)
                        var x1 = Math.max(mouse.x, imgcliprect.x0)
                        var y1 = Math.max(mouse.y, imgcliprect.y0)
                        imgcliprect.x = x0
                        imgcliprect.y = y0
                        imgcliprect.width = x1 - x0
                        imgcliprect.height = y1 - y0
                    }
                }

                onReleased: {
                    if ((imgcliprect.width >= Units.dp(16)) && (imgcliprect.height >= Units.dp(16))) {
                        imgclipdialog.positiveButton.enabled = true
                    }
                }
            }
        }
    ]
}
