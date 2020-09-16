from Qt.QtCore import Qt, Signal, Slot
from Qt.QtWidgets import (
    QComboBox,
    QDataWidgetMapper,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)
from Qt.QtSql import QSqlRelationalDelegate


class InformationWindow(QDialog):
    imageChanged = Signal(int, str)

    def __init__(self, id_, items, parent=None):
        super().__init__(parent)

        itemLabel = QLabel(self.tr("Item: "))
        descriptionLabel = QLabel(self.tr("Description: "))
        imageFileLabel = QLabel(self.tr("Image file: "))

        self.createButtons()

        self.itemText = QLabel()
        self.descriptionEditor = QTextEdit()

        self.imageFileEditor = QComboBox()
        self.imageFileEditor.setModel(items.relationModel(1))
        self.imageFileEditor.setModelColumn(items.relationModel(1).fieldIndex("file"))

        self.mapper = QDataWidgetMapper(self)
        self.mapper.setModel(items)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setItemDelegate(QSqlRelationalDelegate(self.mapper))
        self.mapper.addMapping(self.imageFileEditor, 1)
        self.mapper.addMapping(self.itemText, 2, b"text")
        self.mapper.addMapping(self.descriptionEditor, 3)
        self.mapper.setCurrentIndex(id_)

        self.descriptionEditor.textChanged.connect(self.enableButtons)
        self.imageFileEditor.currentIndexChanged.connect(self.enableButtons)

        formLayout = QFormLayout()
        formLayout.addRow(itemLabel, self.itemText)
        formLayout.addRow(imageFileLabel, self.imageFileEditor)
        formLayout.addRow(descriptionLabel, self.descriptionEditor)

        layout = QVBoxLayout()
        layout.addLayout(formLayout)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        self.itemId = id_
        self.displayedImage = self.imageFileEditor.currentText()

        self.setWindowFlags(Qt.Window)
        self.enableButtons(False)
        self.setWindowTitle(self.itemText.text())

    def id(self):
        return self.itemId

    @Slot()
    def revert(self):
        self.mapper.revert()
        self.enableButtons(False)

    @Slot()
    def submit(self):
        newImage = self.imageFileEditor.currentText()

        if self.displayedImage != newImage:
            self.displayedImage = newImage
            self.imageChanged.emit(self.itemId, newImage)

        self.mapper.submit()
        self.mapper.setCurrentIndex(self.itemId)

        self.enableButtons(False)

    def createButtons(self):

        self.closeButton = QPushButton(self.tr("&Close"))
        self.revertButton = QPushButton(self.tr("&Revert"))
        self.submitButton = QPushButton(self.tr("&Submit"))

        self.closeButton.setDefault(True)

        self.closeButton.clicked.connect(self.close)
        self.revertButton.clicked.connect(self.revert)
        self.submitButton.clicked.connect(self.submit)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.addButton(self.submitButton, QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(self.revertButton, QDialogButtonBox.ResetRole)
        self.buttonBox.addButton(self.closeButton, QDialogButtonBox.RejectRole)

    @Slot()
    @Slot(bool)
    def enableButtons(self, enable=True):
        self.revertButton.setEnabled(enable)
        self.submitButton.setEnabled(enable)
