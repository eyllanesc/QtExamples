import QtQuick 2.15
import QtQuick.Controls 1.4 as QQC1
import QtQuick.Controls.Styles 1.4
import QtQuick.Layouts 1.15

QQC1.ApplicationWindow{
    id: root
    title: "Demo"
    visible: true
    width: 640
    height: 480
    minimumWidth: 300
    QtObject{
        id: _internals
        function calculateWidth(){
            return (view.viewport.width - checkboxColumn.width)/(view.columnCount - 1)
        }
    }
    RowLayout{
        id: rowItem
        width: view.width
        x: 20
        QQC1.SpinBox{
            Layout.fillWidth: true
            Layout.margins: 10
            font.pointSize: 20
        }
        QQC1.SpinBox{
            Layout.fillWidth: true
            Layout.margins: 10
            font.pointSize: 20
        }
        QQC1.Button{
            Layout.margins: 10
            text: "Add"
            Layout.fillWidth: true
            style: ButtonStyle {
                label: Text{
                    text: control.text
                    font.pointSize: 20
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
            }
        }
    }
    QQC1.TableView {
        id: view
        x: rowItem.x
        width: 500
        anchors.top: rowItem.bottom
        height: root.height - rowItem.height - 20
        model: manager ? manager.model : null
        alternatingRowColors: false
        backgroundVisible: false
        QQC1.TableViewColumn{
            id: checkboxColumn
            title: ""
            role: "checked"
            movable: false
            resizable: false
            width: 40
            delegate: Item{
                QQC1.CheckBox{
                    checked: styleData.value
                    anchors.centerIn: parent
                    onCheckedStateChanged: function(){
                        if(manager.model) 
                            manager.model.setChecked(styleData.row, checked)
                    }
                }
            }
        }
        QQC1.TableViewColumn{
            title: "Node"
            role: "name"
            movable: false
            resizable: false
            width: _internals.calculateWidth()
        }
        QQC1.TableViewColumn{
            title: "X"
            role: "x"
            movable: false
            resizable: false
            width: _internals.calculateWidth()
        }
        QQC1.TableViewColumn{
            title: "Y"
            role: "y"
            movable: false
            resizable: false
            width: _internals.calculateWidth()
        }
        rowDelegate: Item{
            height: 35
            Rectangle{
                border.color: "black"
                color: styleData.selected ? "lightgray": "gray"
                anchors.fill: parent
                anchors.margins: 2
            }
        }
        itemDelegate: Item{
            Text{
                anchors.centerIn: parent
                text: styleData.value
                font.pointSize: 15
            }
        }
    }
}