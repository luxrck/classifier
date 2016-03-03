import QtQuick 2.4
import QtQuick.Controls 1.3

import QtMultimedia 5.4

import Material 0.2
import Material.ListItems 0.1 as ListItem
import Material.Extras 0.1

ApplicationWindow {

	id: app

	signal databaseLoad(url dburl)
	signal databaseLoadCancel(url dburl)
	signal databaseLoadComplete(string dbname, url dburl)
	signal databaseChanged(url dburl)

	signal faceClassify(url dburl, url source, var dbimgsize, var threshold, var cliparea)
	signal faceClassifyCancel(url source)
	signal faceClassifyComplete(url source, var result, var preview)

	onDatabaseLoadComplete: {
		imgprocdialog.close()
		settings.databaseLoadComplete(dbname, dburl)
	}

	onFaceClassifyComplete: {
		imgprocdialog.close()

		imgresultdialog.source = source
		imgresultdialog.result = result
		imgresultdialog.preview = preview
		imgresultdialog.show()
	}

	title: "SRC Classifier"

	// width: 800
	// height: 600
	// maximumWidth: 800
	// maximumHeight: 600

	// clientSideDecorations: true

	// flags: Qt.WindowTitleHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint

	initialPage: mainpage

	Page {
		id: mainpage

		title: "SRC Classifier"
		backgroundColor: Palette.colors.black["500"]

		actions: [
			Action {
				name: "Settings"

				// Icon name from the Google Material Design icon pack
				// https://github.com/google/material-design-icons
				iconName: "navigation/menu"

				onTriggered: {

					// Open setting panel
					navsettings.toggle()
				}
			}
		]

		NavigationDrawer {
			id: navsettings

			mode: "right"

			SettingPanel {
				id: settings
				height: parent.height

				onDatabaseLoad: app.databaseLoad(dburl)
				onDatabaseLoadCancel: app.databaseLoadCancel(dburl)
				onDatabaseLoadComplete: {
					settings.dblistadd({"name": dbname, "url": dburl.toString()})
				}
				onDatabaseChanged: app.databaseChanged(dburl)
			}
		}

		Camera {

			id: camera

			captureMode: Camera.CaptureStillImage
			imageProcessing.whiteBalanceMode: CameraImageProcessing.WhiteBalanceFlash

			exposure {
				exposureCompensation: -1.0
				exposureMode: Camera.ExposurePortrait
			}

			digitalZoom: 1.0

			flash.mode: Camera.FlashRedEyeReduction

			imageCapture {

				// resolution: "800x600"

				onImageCaptured: {
					console.log(preview)
					console.log(imageCapture.capturedImagePath)
					//var qmlstr = "import QtQuick 2.4; Image { source: " + preview + "; visible: false }"
					//console.log(qmlstr)
					//var image = Qt.createQmlObject(qmlstr, videosource, "preview1")
					//console.log("onImageCaptured: " + preview + ",,," + settings.db.info.url.toString())
					if (settings.assistmode) {
						imgclipdialog.imgsource = preview
						imgclipdialog.show()
						imgprocdialog.close()
					} else {
						var cliparea = {"x": 0, "y": 0, "width": -1, "height": -1}
						faceClassify(settings.db.info.url, preview, settings.dbimgsize, settings.threshold, cliparea)
					}
				}
			}
		}

		VideoOutput {

			id: videosource

			anchors.fill: parent

			focus : visible // to receive focus and capture key events when visible
			source: camera
		}

		ActionButton {

			id: recognizer

			anchors {
				left: parent.left
				bottom: parent.bottom
				margins: Units.dp(32)
			}

			backgroundColor: Palette.colors.red["500"]

			iconName: "action/work"
			isMiniSize: false

			onClicked: {
				if (!settings.db) {
					infodialog.info = "Error! No database loaded."
					infodialog.show()
				} else {
					imgprocdialog.show()
					camera.imageCapture.captureToLocation("/tmp/preview_1")
					//camera.imageCapture.capture()
				}
			}
		}
	}

	ImageClipDialog {
		id: imgclipdialog
		anchors.fill: parent

		onImageClipped: {
			imgprocdialog.show()
			faceClassify(settings.db.info.url, preview, settings.dbimgsize, settings.threshold, cliparea)
		}
	}

	Dialog {
		id: infodialog

		property alias info: infodialog.text

		positiveButtonText: "Close"
		negativeButton.visible: false
	}

	Dialog {
		id: imgprocdialog

		globalMouseAreaEnabled: false

		positiveButtonText: "Close"
		negativeButton.visible: false

		dialogContent: [
			Row {
				anchors.fill: parent.fill
				spacing: 4

				ProgressCircle {
					anchors {
						verticalCenter: parent.verticalCenter
						margins: 32
					}

					color: Palette.colors.red["500"]
				}

				Label {
					anchors {
						verticalCenter: parent.verticalCenter
						leftMargin: 100
					}

					text: "processing..."
				}
			}
		]
	}

	Dialog {

		id: imgresultdialog

		property alias source: inputimg.source
		property var result: { "class": "", "description": "" }
		property var preview: []

		onPreviewChanged: {
			if (preview.length)	{
				imgpreview1.source = preview[0]
				imgpreview2.source = preview[1]
				imgpreview3.source = preview[2]
			}
		}

		title: "Recognize result"

		positiveButtonText: "Done"
		negativeButton.visible: false

		dialogContent: [
			Row {

				anchors.fill: parent.fill

				spacing: 16

				Image {
					id: inputimg

					width: 160
					height: 120
				}

				Column {

					Label { text: "Class" }

					Text {
						id: imgresultclass

						anchors {
							left: parent.left
							right: parent.right
							leftMargin: Units.dp(8)
						}

						wrapMode: Text.WordWrap
						text: imgresultdialog.result.class
					}

					Label { text: "Description" }

					Text {
						id: imgresultdesc

						anchors {
							left: parent.left
							right: parent.right
							leftMargin: Units.dp(8)
						}

						wrapMode: Text.WrapAnywhere
						text: imgresultdialog.result.description
					}
				}
			},

			Row {

				Image {
					id: imgpreview1

					width: 160
					height: 120
				}

				Image {
					id: imgpreview2

					width: 160
					height: 120
				}

				Image {
					id: imgpreview3

					width: 160
					height: 120
				}
			}
		]
	}
}
