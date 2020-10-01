from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.event import EventDispatcher
from kivy.properties import StringProperty
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup 


from utils import getAvailableEnviroments, getAvailabeCompilers, getAvailablePythons

import subprocess
import os
import sys

class GlobalData(EventDispatcher):
    python = StringProperty("3.6")
    compiler = StringProperty("default")

globals = GlobalData()


def openEnviromentFolder(path):
    subprocess.Popen(r'explorer /select,' + path)

def openCMD(path, compiler):
    subprocess.call(['start', path , compiler], shell = True)

def getPythonPath(path):
    ret_status = subprocess.run([path, "&python.exe", "-c", "import sys;print(sys.executable)"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    path = ret_status.stdout.decode("utf-8")
    part_path = path.partition("python.exe")
    clean_path = part_path[0] + part_path[1]
    return clean_path, ret_status

def getPythonInfo(python):
    python_versions = getAvailablePythons()
    ret_status = subprocess.run([os.path.join(python_versions[python], "python.exe"),"-c", "import sys;print(sys.version)"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return ret_status.stdout, ret_status

def getPipPackages(python):
    python_versions = getAvailablePythons()
    ret_status = subprocess.run([os.path.join(os.path.dirname(python), "pip.exe"),"freeze"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    data = ret_status.stdout.decode("utf-8").split("\r\n")
    return data, ret_status

def createNewEnviroment(name):
    from data import envs
    python_versions = getAvailablePythons()
    enviroment_path = envs[0] 
    ret_status = subprocess.run([os.path.join(python_versions[globals.python], "python.exe"),"-m", "venv", os.path.join(enviroment_path, name)])
    return ret_status

def changeCompiler(x):
    globals.compiler = x

def changePython(x):
    globals.python = x


def changeTextCallback(widget, text):
    widget.text = text

font_size = 14

class CompilerRow(BoxLayout):
    def __init__(self, **kwargs):
        super(CompilerRow, self).__init__()
        self.comp_button = Button(text="Compiler", size_hint_x = 0.3)
        self.label = Label(text = globals.compiler, size_hint_x = 0.7)
        self.dropdown = DropDown()

        for c in getAvailabeCompilers():
            btn = Button(text = c, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)    


        self.dropdown.bind(on_select = lambda  x, y: changeCompiler(y))
        self.dropdown.bind(on_select = lambda  x, y: changeTextCallback(self.label,y))
        self.comp_button.bind(on_release = self.dropdown.open)

        self.add_widget(self.comp_button)
        self.add_widget(self.label)

class PythonVersionRow(BoxLayout):
    def __init__(self, **kwargs):
        super(PythonVersionRow, self).__init__()
        self.comp_button = Button(text="Python Version", size_hint_x = 0.3)
        self.label = Label(text = getPythonInfo(globals.python)[0].decode("utf-8"), size_hint_x = 0.7)
        self.dropdown = DropDown()

        for p in getAvailablePythons():
            btn = Button(text = p, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)    


        self.dropdown.bind(on_select = lambda  x, y: changePython(y))
        self.dropdown.bind(on_select = lambda  x, y: changeTextCallback(self.label,getPythonInfo(y)[0].decode("utf-8")))
        self.comp_button.bind(on_release = self.dropdown.open)

        self.add_widget(self.comp_button)
        self.add_widget(self.label)

class CreateNewEnviromentRow(BoxLayout):
    def __init__(self, **kwargs):
        super(CreateNewEnviromentRow, self).__init__()
        self.btn = Button(text = "Create new enviroment")
        self.textinput = TextInput(text='Enviroment Name', multiline=False)

        def createNewEnvCallback(x):
            createNewEnviroment(self.textinput.text.replace(" ", "_"))
        
        self.btn.bind(on_release = createNewEnvCallback)
        self.add_widget(self.btn)

        self.add_widget(self.textinput)

class MenuRow(BoxLayout):
    def __init__(self, **kwargs):
        super(MenuRow, self).__init__()

        self.add_widget(CompilerRow())
        self.add_widget(PythonVersionRow())
        self.add_widget(CreateNewEnviromentRow())
        
        


class EnviromentEntry(BoxLayout):
    def __init__(self, **kwargs):
        super(EnviromentEntry, self).__init__()

        self.enviroment = kwargs["enviroment"]

        def openPopUpCallback(x):
            layout = GridLayout(cols = 1)
            environments = getAvailableEnviroments()
            python_path, _ = getPythonPath(environments[self.enviroment])
            pip_packages, _ = getPipPackages(python_path)
            popup = Popup(title = self.enviroment + " pip packages", size_hint = (0.5,1.0), content = layout)   
            for pip_package in pip_packages:
                layout.add_widget(Label(text = pip_package, size_hint_y = 0.1))
            popup.open()    


        self.enviroment_button = Button(text=self.enviroment, size_hint = (0.6,1))
        self.enviroment_button.bind(on_release = openPopUpCallback)
        self.add_widget(self.enviroment_button)

        self.open_cmd_btn = Button(text="cmd", size_hint = (0.2,1))

        def openCMDCallback(instance):
            environments = getAvailableEnviroments()
            openCMD(environments[self.enviroment], globals.compiler)

        self.open_cmd_btn.bind(on_release = openCMDCallback)
        self.add_widget(self.open_cmd_btn)


        def openDirCallback(instance):
            environments = getAvailableEnviroments()
            openEnviromentFolder(os.path.dirname(environments[self.enviroment]))

        self.open_dir_btn = Button(text="op", size_hint = (0.2,1))
        self.open_dir_btn.bind(on_release = openDirCallback)
        self.add_widget(self.open_dir_btn)



class EnviromentsList(BoxLayout):
    def __init__(self, **kwargs):
        super(EnviromentsList, self).__init__(**kwargs)
        self.buttons = [EnviromentEntry(enviroment = enviroment) for enviroment in getAvailableEnviroments()]
        for button in self.buttons:
            self.add_widget(button)


class Program(BoxLayout):
    def __init__(self, **kwargs):
        super(Program, self).__init__(**kwargs)

        self.add_widget(MenuRow())
        self.add_widget(EnviromentsList())

class MyScreen(Screen):
    def __init__(self, **kwargs):
        super(MyScreen, self).__init__(**kwargs)
        self.add_widget(Program())

class TestApp(App):
    def build(self):
        self.sm = ScreenManager() # transition = NoTransition())
        self.sm.add_widget(MyScreen())
        return self.sm
 

TestApp().run()