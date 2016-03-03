import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Dialogs 1.2
import QtQuick.Layouts 1.1

import Material 0.2
import Material.ListItems 0.1 as ListItem
import Material.Extras 0.1

View {

	id: settingPanel

	property alias db: dblistview.currentItem
	property size dbimgsize: Qt.size(dbimgsize.value, dbimgsize.value)
	property alias threshold: srcthreshold.value
	property var assistmode: assist.checked

	signal databaseLoad(url dburl)
	signal databaseLoadCancel(url dburl)
	signal databaseLoadComplete(string dbname, url dburl)
	signal databaseChanged(url dburl)

	function dblistadd(value) {
		dbmodel.append({"name": value.name, "url": value.url})
	}

	anchors.fill: parent

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
		spacing: Units.dp(16)

		ListItem.Subheader {
			text: "Face Database"
			style: "subheading"
		}

		ListView {

				id: dblistview

				width: parent.width
				height: (dblistview.count >= 5 ? 5 : dblistview.count) * Units.dp(32)

				model: dbmodel
				delegate: dbdelegate

				onCurrentItemChanged: {
					dbgroup.current = dblistview.currentItem.radio
				}

				ExclusiveGroup { id: dbgroup }

				ListModel { id: dbmodel }

				Component {

					id: dbdelegate

					RowLayout {

						id: dblistitem

						property var info: {"name": name, "url": url}
						property alias radio: dbradio

						width: settingPanel.width - Units.dp(16)
						height: Units.dp(32)

						RadioButton {

							id: dbradio

							Layout.fillWidth: true
							Layout.fillHeight: true
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

							Layout.alignment: Qt.AlignRight

							size: Units.dp(16)

							iconName: "navigation/close"
							hoverAnimation: true

							onClicked: {
								var item = dblistview.indexAt(dbradioclose.x, dbradioclose.y)
								console.log(item)
								dbmodel.remove(item)
								dblistview.currentItem = null
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
				//dbmodel.append({"name": "attfaces", "url": "db://attfaces"})
				//dbmodel.append({"name": "yalebfaces"})
				//dbmodel.append({"name": "attfaces"})
			}
		}

		ListItem.Subtitled {

			id: dbimgsetting

			text: "Database Image Size"
			valueText: dbimgsize.value ? "(" + dbimgsize.value + "x" + dbimgsize.value + ")" : ""
			showDivider: true

			content: Slider {

				id: dbimgsize

				//anchors.horizontalCenter: parent.horizontalCenter
				//width: parent.width - Units.dp(32)
				width: parent.width

				value: 16
				stepSize: 1
				minimumValue: 15
				maximumValue: 30

				tickmarksEnabled: true
			}
		}

		ListItem.Subtitled {

			text: "Threshold"
			valueText: String(srcthreshold.value.toFixed(2))
			showDivider: true

			content: Slider {

				id: srcthreshold

				//anchors.horizontalCenter: parent.horizontalCenter

				//width: parent.width - Units.dp(32)
				anchors.fill: parent

				value: 0.5
				stepSize: 0.05
				minimumValue: 0
				maximumValue: 1

				//focus: true
				//activeFocusOnPress: true
				tickmarksEnabled: true
				numericValueLabel: true
			}
		}

		ListItem.Subtitled {
			text: "Assistant Mode"
			subText: "User should select recognition area manually"
			maximumLineCount: 3
			secondaryItem: Switch {
				id: assist
				anchors.verticalCenter: parent.verticalCenter
			}
			onClicked: assist.checked = !assist.checked
		}
	}
}
