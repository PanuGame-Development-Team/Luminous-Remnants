from PySide6.QtWidgets import *
from PySide6 import QtUiTools
from sys import argv
from inspect import getmembers
from settings import *
from json import dumps,loads
RANGE = {"INIT.FOOTNOTE_FONT_SIZE":[12,48],
         
         "GENERAL.GRAPH_WIDTH":[1,1024],
         "GENERAL.VISIBLE_DISTANCE":[150.0,100000.0],

         "GALAXY.LINE_SHOW_FACTOR":[255,100000],
         "GALAXY.LABEL_DISPSIZE":[10,1000],
         "GALAXY.LABEL_SHOW_FACTOR":[255,100000],

         "STAR.ROTATION":[0.1,10.0],
         "STAR.RADIUS":[3.0,50.0],
         "STAR.RADIUS_FACTOR":[1.0,2.0],
         "STAR.SHOW_FACTOR":[255,100000],
         "STAR.HOVER_TICK":[10,100],

         "PICTURE.ALPHA_DECAY":[1.0,10.0],
         "PICTURE.MAX_ALPHA":[255,255],

         "CONTROLLER.HOVER_DISTANCE_SQ":[150.0,100000.0],
         "CONTROLLER.ROTATE_TICK":[5,100],

         "HANDLER.SPEED_CONTROL_FACTOR":[0.5,1.0],
         "HANDLER.AUTOPLAY.MAX_LOOP":[1,100000],
         "HANDLER.AUTOPLAY.SCROLL_BG_FACTOR":[0.05,0.8],
         "HANDLER.AUTOPLAY.TIME.MOVEMOUSE":[0.3,5.0],
         "HANDLER.AUTOPLAY.TIME.FADE":[0.5,10.0],
         "HANDLER.AUTOPLAY.TIME.CACHE":[0.3,5.0],

         "METEOR.MIN_LENGTH":[50,3000],
         "METEOR.MAX_LENGTH":[50,3000],
         "METEOR.MIN_DIRECTION":[0,180],
         "METEOR.MAX_DIRECTION":[0,180],
         "METEOR.FROMY_FACTOR":[0.0,1.0],
         "METEOR.STAY_TICK":[30,480],
         "METEOR.SLIDE_TICK":[30,480],
         "METEOR.SHOW_FACTOR":[255,100000],
         "METEOR.FRONT_STAR_RADIUS":[3.0,50.0],
         "METEOR.BACK_STAR_RADIUS":[3.0,50.0],
         "METEOR.ROTATION":[0.1,10.0],
         "METEOR.FRONT_COVER_RADIUS":[3.0,50.0],
         "METEOR.BACK_COVER_RADIUS":[3.0,50.0],

         "METEOR.RAIN.MIN_PROBABILITY":[0.001,0.1],
         "METEOR.RAIN.MAX_PROBABILITY":[0.001,0.1],
         "METEOR.RAIN.PROBABILITY_PERIOD":[60,100000],
         "METEOR.RAIN.SPACING_TICK":[60,1200],
         "METEOR.RAIN.METEOR_LIMIT":[1,100000],
         "METEOR.RAIN.DURATION":[300,100000],
         "METEOR.RAIN.TICK_PER_MET":[1,36]
         }

class MainWindow(*QtUiTools.loadUiType("customize_settings.ui")):
    dic = {}
    path = []
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.tab:QTabWidget
        for i in range(self.tab.count()):
            self.path.append(self.tab.widget(i).objectName().upper())
            object = globals()[self.tab.widget(i).objectName().upper()]
            widget = self.create_control(object)
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setWidget(widget)
            QGridLayout(self.tab.widget(i))
            self.tab.widget(i).layout().addWidget(scroll)
            scroll.setParent(self.tab.widget(i))
            self.path.pop()
    def gen_layout(self,WRAPPER,widget):
        layout = QFormLayout(widget)
        layout.setVerticalSpacing(0)
        for name,value in getmembers(WRAPPER):
            if name.startswith("__"):
                continue
            if name == "ENABLE":
                continue
            label = QLabel(name)
            self.path.append(name)
            control = self.create_control(value)
            self.path.pop()
            control.setToolTip(f"修改前: {value}")
            layout.addRow(label,control)
    def create_control(self,value) -> QWidget:
        if isinstance(value,bool):
            control = QCheckBox()
            control.setChecked(value)
            self.gen_hook(control)
        elif isinstance(value,int):
            control = QSpinBox()
            if RANGE.get(".".join(self.path)):
                control.setRange(*RANGE[".".join(self.path)])
            control.setValue(value)
            self.gen_hook(control)
        elif isinstance(value,float):
            control = QDoubleSpinBox()
            if RANGE.get(".".join(self.path)):
                control.setRange(*RANGE[".".join(self.path)])
            control.setValue(value)
            control.setDecimals(9)
            self.gen_hook(control)
        elif isinstance(value,list):
            control = QLineEdit()
            control.setText(dumps(value))
        elif hasattr(value,"ENABLE"):
            control = QGroupBox()
            control.setCheckable(True)
            control.setChecked(getattr(value,"ENABLE"))
            control.setFlat(True)
            control.setTitle("ENABLE")
            self.path.append("ENABLE")
            self.gen_hook(control)
            self.path.pop()
            self.gen_layout(value,control)
        else:
            control = QWidget()
            self.gen_layout(value,control)
        return control
    def gen_hook(self,control):
        self.dic[".".join(self.path)] = control
    def closeEvent(self,a0):
        result = QMessageBox.question(self,"保存星图","是否要保存星图",QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
        if result == QMessageBox.Yes:
            self.save()
            a0.accept()
        elif result == QMessageBox.No:
            a0.accept()
        else:
            a0.ignore()
    def save(self):
        properties = []
        section = "GENERAL"
        for pathstr in self.dic:
            path = pathstr.split(".")
            if path[0] != section:
                section = path[0]
                properties.append(f"[{section}]")
            val = self.val(self.dic[pathstr])
            if val:
                properties.append(".".join(path[1:]) + "=" + val)
        with open("properties","w") as file:
            file.write("\n".join(properties))
    def val(self,control:QWidget):
        if isinstance(control,QLineEdit):
            str = dumps(loads(control.text()))
        elif isinstance(control,QCheckBox):
            str = dumps(bool(control.isChecked()))
        elif isinstance(control,QGroupBox):
            str = dumps(bool(control.isChecked()))
        elif isinstance(control,QSpinBox):
            str = dumps(control.value())
        elif isinstance(control,QDoubleSpinBox):
            str = dumps(control.value())
        return str
app = QApplication(argv)
window = MainWindow()
window.show()
app.exec()