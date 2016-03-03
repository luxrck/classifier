import QtQuick 2.5
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.2

import QtMultimedia 5.5

import Material 0.2
import Material.ListItems 0.1 as ListItem
import Material.Extras 0.1

Dialog {
	id: imgclipdialog

	signal imageClipped(var preview, var cliparea)
	property alias imgsource: imgpreview.source

	title: "  "

	positiveButtonText: "Next"
	positiveButton.enabled: false
	negativeButton.visible: false

	// interactive: false

	onOpened: {
		imgcliprect.x = imgcliprect.x0 = 0
		imgcliprect.y = imgcliprect.y0 = 0
		imgcliprect.width = imgcliprect.height = 0
		positiveButton.enabled = false
	}

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
			fillMode: Image.PreserveAspectFit

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
						var s0 = imgpreview.sourceSize
						var x0 = Math.min(mouse.x, imgcliprect.x0)
						var y0 = Math.min(mouse.y, imgcliprect.y0)
						x0 = Math.max(x0, 0)
						y0 = Math.max(y0, 0)
						var x1 = Math.max(mouse.x, imgcliprect.x0)
						var y1 = Math.max(mouse.y, imgcliprect.y0)
						x1 = Math.min(x1, imgpreview.width)
						y1 = Math.min(y1, imgpreview.height)
						imgcliprect.x = x0
						imgcliprect.y = y0
						imgcliprect.width = x1 - x0
						imgcliprect.height = y1 - y0
						console.log(x0,y0,x1,y1, s0, imgpreview.width, imgpreview.height)
					}
				}

				onReleased: {
					if ((imgcliprect.width >= Units.dp(16)) && (imgcliprect.height >= Units.dp(16))) {
						imgclipdialog.positiveButton.enabled = true
					} else {
						imgclipdialog.positiveButton.enabled = false
					}
				}
			}

			Rectangle {
				id: imgcliprect

				property var x0: 0
				property var y0: 0

				color: Qt.rgba(0, 0, 0, 0.5)

				Drag.active: imgcliparea.drag.active
				Drag.hotSpot.x: 10
				Drag.hotSpot.y: 10

				MouseArea {
					id: imgcliparea

					property var px: 0
					property var py: 0

					anchors.fill: parent
					drag.target: parent
				}
			}
		}
	]
}
