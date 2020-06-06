from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication, QLabel, QScrollArea, QVBoxLayout, QWidget
from PyQt5.QtSerialPort import QSerialPortInfo


def main():
    import sys

    app = QApplication(sys.argv)

    layout = QVBoxLayout()

    infos = QSerialPortInfo.availablePorts()
    for info in infos:
        s = (
            f"Port: {info.portName()}",
            f"Location: {info.systemLocation()}",
            f"Description: {info.description()}",
            f"Manufacturer: {info.manufacturer()}",
            f"Serial number: {info.serialNumber()}",
            "Vendor Identifier: " + f"{info.vendorIdentifier():x}"
            if info.hasVendorIdentifier()
            else "",
            "Product Identifier: " + f"{info.productIdentifier():x}"
            if info.hasProductIdentifier()
            else "",
        )
        label = QLabel("\n".join(s))
        layout.addWidget(label)

    workPage = QWidget()
    workPage.setLayout(layout)

    area = QScrollArea()
    area.setWindowTitle("Info about all available serial ports.")
    area.setWidget(workPage)
    area.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
