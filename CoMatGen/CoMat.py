"""
Source code for COMat: Input file generator for COncrete damaged plasticity Material model in Abaqus

Author: Youngbin LIM
Contact: lyb0684@naver.com
"""
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget,
                             QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog,
                             QHBoxLayout, QGridLayout, QDesktopWidget, QMessageBox, QCheckBox)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import sys
import os
import COMat_Generator

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'CoMat - Developed by Youngbin LIM'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 900, 600)

        self.tab_widget = MyTabWidget(self)

        # Create a central widget for the QMainWindow layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create a vertical layout for the central widget
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.addWidget(self.tab_widget)

        # Create and add buttons to the layout
        self.createButtons()
        self.main_layout.addLayout(self.button_layout)

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
        # Set the window icon
        Icon_Path = os.path.join(os.path.dirname(__file__), 'Icon', 'CoMat_Icon.ico')
        self.setWindowIcon(QIcon(Icon_Path))
        
        self.show()

    def createButtons(self):
        self.plot_button = QPushButton("Plot Graph")
        self.generate_button = QPushButton("Generate Input File")
        self.info_button = QPushButton("Show Usage Hints")
    
        # Connect the buttons to their respective slots
        self.plot_button.clicked.connect(self.tab_widget.handlePlotButtonClick)
        self.generate_button.clicked.connect(self.tab_widget.handleGenerateButtonClick)
        self.info_button.clicked.connect(self.showUsageHintsWindow)  # Connect to the new method
    
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.plot_button)
        self.button_layout.addWidget(self.generate_button)
        self.button_layout.addWidget(self.info_button)
        
        self.developer_button = QPushButton("Developer")
        self.developer_button.clicked.connect(self.showDeveloperWindow)
        self.button_layout.addWidget(self.developer_button)
        
    def showUsageHintsWindow(self):
        self.usage_hints_window = UsageHintsWindow()
        self.usage_hints_window.show()
        
    def showDeveloperWindow(self):
        self.developer_window = DeveloperWindow()
        self.developer_window.show()

class DeveloperWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'Developer Info'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(800, 500, 350, 150)

        # Set the background color to white
        self.setStyleSheet("background-color: white;")

        # Create a QLabel to display the developer's introduction and hyperlinks
        label = QLabel(self)
        
        # Set the font family and size
        font = QFont("Times New Roman", 10)
        label.setFont(font)

        # Arrange the hyperlinks horizontally and set the text
        label.setText("""
            <p>Developer: Youngbin LIM</p>
            <p>Contact: lyb0684@naver.com</p>
            <p style="text-align:center;">
                <a href="https://blog.naver.com/lyb0684">Blog</a> |
                <a href="https://www.linkedin.com/in/lyb0684/">LinkedIn</a> |
                <a href="https://github.com/YB-LIM">GitHub</a>
            </p>
        """)
        
        label.setOpenExternalLinks(True)
        label.setAlignment(Qt.AlignCenter)

        # Set the QLabel as the central widget
        self.setCentralWidget(label)
        
        # Set the window icon
        Icon_Path = os.path.join(os.path.dirname(__file__), 'Icon', 'CoMat_Icon.ico')
        self.setWindowIcon(QIcon(Icon_Path))
        

class UsageHintsWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'Usage Hints - Developed by Youngbin LIM'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(300, 200, 600, 400)
    
        self.tab_widget = QTabWidget(self)
    
        # Create tabs
        self.compressionTab = QWidget()
        self.tensionTab = QWidget()
    
        self.tab_widget.addTab(self.compressionTab, "Compression")
        self.tab_widget.addTab(self.tensionTab, "Tension")
    
        # Load images for Compression sub-tabs
        compression_images = [
            os.path.join(os.path.dirname(__file__), 'Figs', 'Compression_Sub_Tab_1.png'),
            os.path.join(os.path.dirname(__file__), 'Figs', 'Compression_Sub_Tab_2.png'),
            os.path.join(os.path.dirname(__file__), 'Figs', 'Compression_Sub_Tab_3.png'),
            os.path.join(os.path.dirname(__file__), 'Figs', 'Compression_Sub_Tab_4.png'),
            os.path.join(os.path.dirname(__file__), 'Figs', 'Compression_Sub_Tab_5.png'),
            os.path.join(os.path.dirname(__file__), 'Figs', 'Compression_Sub_Tab_6.png'),
        ]
    
        # Create sub-tabs for Compression tab
        self.compressionSubTabs = QTabWidget(self.compressionTab)
        self.compressionSubTabs.setTabPosition(QTabWidget.West)  # Set tab position to the left
        for i in range(1, 7):
            subTab = QWidget()
            subTab.layout = QVBoxLayout(subTab)
    
            # Load and set the image
            pixmap = QPixmap(compression_images[i-1])
            pixmap = pixmap.scaled(1000, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Set the size of the image
            lbl = QLabel(self)
            lbl.setPixmap(pixmap)
            subTab.layout.addWidget(lbl)
            subTab.setLayout(subTab.layout)
            self.compressionSubTabs.addTab(subTab, str(i))
        
        compressionLayout = QVBoxLayout(self.compressionTab)
        compressionLayout.addWidget(self.compressionSubTabs)
        self.compressionTab.setLayout(compressionLayout)
    
        # Load images for Tension sub-tabs
        tension_images = [
            os.path.join(os.path.dirname(__file__), 'Figs', 'Tension_Sub_Tab_1.png'),
            os.path.join(os.path.dirname(__file__), 'Figs', 'Tension_Sub_Tab_2.png'),
            os.path.join(os.path.dirname(__file__), 'Figs', 'Tension_Sub_Tab_3.png'),
            os.path.join(os.path.dirname(__file__), 'Figs', 'Tension_Sub_Tab_4.png'),
            os.path.join(os.path.dirname(__file__), 'Figs', 'Tension_Sub_Tab_5.png'),
            os.path.join(os.path.dirname(__file__), 'Figs', 'Tension_Sub_Tab_6.png'),
            os.path.join(os.path.dirname(__file__), 'Figs', 'Tension_Sub_Tab_7.png'),
        ]
    
        # Create sub-tabs for Tension tab
        self.tensionSubTabs = QTabWidget(self.tensionTab)
        self.tensionSubTabs.setTabPosition(QTabWidget.West)  # Set tab position to the left
        for i in range(1, 6):
            subTab = QWidget()
            subTab.layout = QVBoxLayout(subTab)
        
            # Load and set the image
            pixmap = QPixmap(tension_images[i-1])
            pixmap = pixmap.scaled(1000, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Set the size of the image
            lbl = QLabel(self)
            lbl.setPixmap(pixmap)
            subTab.layout.addWidget(lbl)        
            subTab.setLayout(subTab.layout)
            self.tensionSubTabs.addTab(subTab, str(i))
    
        tensionLayout = QVBoxLayout(self.tensionTab)
        tensionLayout.addWidget(self.tensionSubTabs)
        self.tensionTab.setLayout(tensionLayout)
    
        # Set the main tab widget as the central widget
        self.setCentralWidget(self.tab_widget)

        # Set the window icon
        Icon_Path = os.path.join(os.path.dirname(__file__), 'Icon', 'CoMat_Icon.ico')
        self.setWindowIcon(QIcon(Icon_Path))
    
        self.show()

class MyTabWidget(QTabWidget):
    def __init__(self, parent):
        super(MyTabWidget, self).__init__(parent)
        self.parent = parent
        self.file_save_path_edit = None
        self.initUI()

    def initUI(self):
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
    
        self.addTab(self.tab1, "Compression")
        self.addTab(self.tab2, "Tension")
        self.addTab(self.tab3, "File Save Path")

        self.createCompressionTab()
        self.createTensileTab()
        self.createFileSavePathTab()

    def handlePlotButtonClick(self):
        try:
            Path = self.file_save_path_edit.text()
            is_meter = self.is_meter_checkbox.isChecked()
            Plot_Graph = True
        
            E = float(self.compression_line_edits[0].text())
            S_cu = float(self.compression_line_edits[1].text())
            e_cu = float(self.compression_line_edits[2].text())
            e_60 = float(self.compression_line_edits[3].text())
            Alpha = float(self.compression_line_edits[4].text())
            Tension_Recovery = float(self.compression_line_edits[5].text())

            S_tu = float(self.tensile_line_edits[0].text())
            e_end = float(self.tensile_line_edits[1].text())
            Beta = float(self.tensile_line_edits[2].text())
            Compression_Recovory = float(self.tensile_line_edits[3].text())
            Ref_Length = float(self.tensile_line_edits[4].text())
            COMat_Generator.plot(Path, Plot_Graph, E, S_cu, e_cu, e_60, Alpha, S_tu, e_end, Beta, Tension_Recovery, Compression_Recovory, is_meter, Ref_Length)

        except ValueError as ve:
            QMessageBox.critical(self, "Error", str(ve))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def handleGenerateButtonClick(self):
        try:
            Path = self.file_save_path_edit.text()
            is_meter = self.is_meter_checkbox.isChecked()
            Plot_Graph = True
            
            E = float(self.compression_line_edits[0].text())
            S_cu = float(self.compression_line_edits[1].text())
            e_cu = float(self.compression_line_edits[2].text())
            e_60 = float(self.compression_line_edits[3].text())
            Alpha = float(self.compression_line_edits[4].text())
            Tension_Recovery = float(self.compression_line_edits[5].text())

            S_tu = float(self.tensile_line_edits[0].text())
            e_end = float(self.tensile_line_edits[1].text())
            Beta = float(self.tensile_line_edits[2].text())
            Compression_Recovory = float(self.tensile_line_edits[3].text())
            Ref_Length = float(self.tensile_line_edits[4].text())

            COMat_Generator.generate(Path, Plot_Graph, E, S_cu, e_cu, e_60, Alpha, S_tu, e_end, Beta, Tension_Recovery, Compression_Recovory, is_meter, Ref_Length)
            QMessageBox.information(self, "Success", "Input File generated successfully!")
       
        except ValueError as ve:
            QMessageBox.critical(self, "Error", str(ve))
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def createCompressionTab(self):
        self.tab1.layout = QGridLayout(self)
        self.tab1.layout.setVerticalSpacing(0)
        font = QFont("Times New Roman", 13)

        parameters = [
            (" <i>E</i> (GPa):", "30.0"),
            (" <i>σ</i><sub>cu</sub> (MPa):", "50.0"),
            (" <i>ε</i><sub>cu</sub>:", "0.003"),
            (" <i>ε</i><sub>0.63</sub>:", "0.005"),
            (" <i>α</i>:", "2.0"),
            (" <i>w</i><i><sub>t</sub></i>:", "1.0"),
        ]
        
        self.compression_line_edits = [] 

        for i, (param, default_value) in enumerate(parameters):
            label = QLabel(param)
            label.setFont(font)
            self.tab1.layout.addWidget(label, i, 0)
            line_edit = QLineEdit(self)
            line_edit.setText(default_value)
            self.tab1.layout.addWidget(line_edit, i, 1)
            self.compression_line_edits.append(line_edit)
            
        img_path = os.path.join(os.path.dirname(__file__), 'Figs', 'Compressive_SS_Description.png')
        pixmap = QPixmap(img_path)
        pixmap = pixmap.scaled(800, 470, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)
        self.tab1.layout.addWidget(lbl, 0, 2, len(parameters), 1)

        self.tab1.setLayout(self.tab1.layout)

    def createTensileTab(self):
        self.tab2.layout = QGridLayout(self)
        self.tab2.layout.setVerticalSpacing(5)
        font = QFont("Times New Roman", 13)

        parameters = [
            ("<i>σ</i><sub>tu</sub> (MPa):", "5.0"),
            ("<i>ε</i><sub>end</sub>:", "0.002"),
            ("<i>β</i>:", "2.0"),
            ("<i>w</i><i><sub>c</sub></i>:", "0.0"),
            ("<i>l</i><sub>ref</sub>:", "1.0"),
        ]
        
        self.tensile_line_edits = []
        
        for i, (param, default_value) in enumerate(parameters):
            label = QLabel(param)
            label.setFont(font)
            self.tab2.layout.addWidget(label, i, 0)
            line_edit = QLineEdit(self)
            line_edit.setText(default_value)
            self.tab2.layout.addWidget(line_edit, i, 1)
            self.tensile_line_edits.append(line_edit)
           
        img_path = os.path.join(os.path.dirname(__file__), 'Figs', 'Tensile_SS_Description.png')
        pixmap = QPixmap(img_path)
        pixmap = pixmap.scaled(800, 470, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)
        self.tab2.layout.addWidget(lbl, 0, 2, len(parameters), 1)

        self.tab2.setLayout(self.tab2.layout)

    def createFileSavePathTab(self):
        self.tab3.layout = QVBoxLayout(self)
        font = QFont("Times New Roman", 10)

        # Create a horizontal layout for the "File Save Path" section
        file_save_layout = QHBoxLayout()
    
        label = QLabel("File save path:")
        label.setFont(font)
        file_save_layout.addWidget(label)
        
        self.file_save_path_edit = QLineEdit(self)
        if self.file_save_path_edit is not None:  # Check if file_save_path_edit is not None
            script_directory = os.path.dirname(os.path.abspath(__file__))
            self.file_save_path_edit.setText(script_directory)
            file_save_layout.addWidget(self.file_save_path_edit)
            
        self.file_dialog_button = QPushButton("Select", self)
        self.file_dialog_button.clicked.connect(self.openFileNameDialog)
        file_save_layout.addWidget(self.file_dialog_button)
        
        # Add the horizontal layout to the main vertical layout
        self.tab3.layout.addLayout(file_save_layout)
        
        # Create a checkbox for is_meter parameter and add it to a new horizontal layout
        checkbox_layout = QHBoxLayout()
        self.is_meter_checkbox = QCheckBox("Dimension is in meter", self)
    
        # Set the font size and style for the checkbox
        font = QFont("Times New Roman", 10)
        font.setPointSize(10)  # Set the font size
        #font.setBold(True)  # Set the font style to bold
        self.is_meter_checkbox.setFont(font)
        checkbox_layout.addWidget(self.is_meter_checkbox)
        checkbox_layout.addStretch(1)  # Add stretch to center the checkbox horizontally
        
        self.tab3.layout.addLayout(checkbox_layout)  # Add the checkbox layout to the main vertical layout
        
        self.tab3.setLayout(self.tab3.layout)

    def showUsageHintsWindow(self):
        self.usage_hints_window = UsageHintsWindow()
        self.usage_hints_window.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(self, "Select Save Directory", "", options=options)
        if directory:
            self.file_save_path_edit.setText(directory)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

