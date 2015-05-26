import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Dialogs 1.2
import QtQuick.Layouts 1.1

import Material 0.1
import Material.ListItems 0.1 as ListItem
import Material.Extras 0.1

View {

	id: settingPanel

	property alias db: dblistview.currentItem
	property size dbimgsize: Qt.size(dbimgsize.value, dbimgsize.value)
	property alias threshold: srcthreshold.value

	signal databaseLoad(url dburl)
	signal databaseLoadCancel(url dburl)
	signal databaseLoadComplete(string dbname, url dburl)
	signal databaseChanged(url dburl)

	function dblistadd(value) {
		dbmodel.append({"name": value.name, "url": value.url})
	}

	anchors {
		fill: parent
		margins: Units.dp(8)
	}

	FileDialog {

		id: filedialog
	
		title: "Please choose a file"

		selectExisting: true
		selectFolder: true
		selectMultiple: false
	
		onAccepted: {
			console.log("You chose: " + filedialog.folder)
			databaseLoad(filedialog.fileUrl)
		}

		onRejected: {
			console.log("Canceled")
			filedialog.close()
		}
	}

	Column {
	
		anchors.fill: parent

		ListItem.Subheader { id: dblistheader; text: "Face Database" }

		ListView {

			id: dblistview

			width: parent.width
			height: (dblistview.count >= 5 ? 5 : dblistview.count) * Units.dp(36)

			model: dbmodel
			delegate: dbdelegate

			ExclusiveGroup { id: dbgroup }

			ListModel { id: dbmodel }

			Component {

				id: dbdelegate

				RowLayout {

					id: dblistitem

					property var info: {"name": name, "url": url}

					width: settingPanel.width
					height: Units.dp(32)

					RadioButton {

						id: dbradio

						Layout.alignment: Qt.AlignLeft
						
						exclusiveGroup: dbgroup
						text: name

						Tooltip {
							text: url.toString()
							mouseArea: dbradiomousearea
						}

						MouseArea {
							id: dbradiomousearea
							
							anchors.fill: parent
							hoverEnabled: true
						}
					}

					IconButton {
						
						id: dbradioclose

						property var dbname: dbradio.text

						Layout.alignment: Qt.AlignRight

						iconName: "navigation/close"
						hoverAnimation: true

						onClicked: {
							var item = dblistview.indexAt(dbradioclose.x, dbradioclose.y)
							console.log(item)
							dbmodel.remove(item)
						}
					}
				}
			}
		}

		IconButton {

			id: dbadd

			anchors.horizontalCenter: parent.horizontalCenter

			iconName: "content/add"
			hoverAnimation: true

			onClicked: {
				filedialog.open()
				//dbmodel.append({"name": "attfaces"})
				//dbmodel.append({"name": "yalebfaces"})
				//dbmodel.append({"name": "attfaces"})
			}
		}

		ListItem.Subheader { text: "Database Image Size" }
		
		Text {

			id: dbimgsizetxt

			anchors {
				left: parent.left
				leftMargin: Units.dp(16)
			}
		}

		Slider {

			id: dbimgsize

			anchors.horizontalCenter: parent.horizontalCenter

			width: parent.width - Units.dp(32)

			value: 16
			stepSize: 1
			minimumValue: 15
			maximumValue: 30

			tickmarksEnabled: true

			onValueChanged: {
				dbimgsizetxt.text = "(" + value + "x" + value + ")"
			}
		}

		ListItem.Subheader { text: "Threshold" }

		Slider {

			id: srcthreshold

			anchors.horizontalCenter: parent.horizontalCenter

			width: parent.width - Units.dp(32)

			value: 0.5
			stepSize: 0.05
			minimumValue: 0
			maximumValue: 1

			focus: true
			activeFocusOnPress: true
			tickmarksEnabled: true
			numericValueLabel: true
		}
	}
}