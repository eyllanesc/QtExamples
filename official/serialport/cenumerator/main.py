from Qt.QtCore import QByteArray, QCoreApplication, QFile, QIODevice, QTextStream
from Qt.QtSerialPort import QSerialPortInfo


def main():
    import sys

    app = QCoreApplication(sys.argv)  # noqa: F841
    f = QFile()
    f.open(sys.stdout.fileno(), QIODevice.WriteOnly)
    out = QTextStream(f)
    serialPortInfos = QSerialPortInfo.availablePorts()

    out << "Total number of ports available: " << len(serialPortInfos) << "\n"

    blankString = "N/A"
    description = ""
    manufacturer = ""
    serialNumber = ""

    for serialPortInfo in serialPortInfos:
        description = serialPortInfo.description()
        manufacturer = serialPortInfo.manufacturer()
        serialNumber = serialPortInfo.serialNumber()
        out << "\nPort: " << serialPortInfo.portName() << "\nLocation: " << serialPortInfo.systemLocation() << "\nDescription: " << (  # noqa: E501
            description if description else blankString
        ) << "\nManufacturer: " << (
            manufacturer if manufacturer else blankString
        ) << "\nSerial number: " << (
            serialNumber if serialNumber else blankString
        ) << "\nVendor Identifier: " << (
            QByteArray.number(serialPortInfo.vendorIdentifier(), 16)
            if serialPortInfo.hasVendorIdentifier()
            else blankString
        ) << "\nProduct Identifier: " << (
            QByteArray.number(serialPortInfo.productIdentifier(), 16)
            if serialPortInfo.hasProductIdentifier()
            else blankString
        ) << "\n"


if __name__ == "__main__":
    main()
