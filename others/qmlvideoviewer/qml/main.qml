import QtQuick 2.15
import QtQuick.Window 2.15
import QtMultimedia 5.15
import qutevideo 1.0

Window {
    visible: true
    width: 640
    height: 480
    title: qsTr("Video Viewer")

    QtObject{
        id: _internals
        property var source: openCVSource
    }

    VideoOutput {
        id: video
        anchors.fill: parent
        anchors.margins: 10
        fillMode: VideoOutput.Stretch
        source: _internals.source
        filters: [
            ObjectsFilter{
                /*onObjectsDetected: function(objects){
                    repeater.model = objects
                }*/
            }
        ]

        Repeater{
            id: repeater
            Rectangle{
                property rect r: video.mapNormalizedRectToItem(model.modelData)
                x: r.x
                y: r.y
                width: r.width
                height: r.height
                color: "transparent"
                border.color: "green"
                border.width: 5
            }
        }
    }

    CVSource{
        id: openCVSource
        source: 0
    }

    MSSSource{
        id: mssSource
        source: -1
    }

    Component.onCompleted: () => _internals.source.start()
    Component.onDestruction: () =>  _internals.source.stop()
}
