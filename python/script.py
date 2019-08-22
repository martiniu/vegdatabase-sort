import requests
import json
import sys
from pprint import pprint
import webbrowser
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QMainWindow, QMessageBox, QLabel, QTabWidget
from PyQt5.QtCore import pyqtSlot

# Drammen  -> Oslo
# 86512932 -> 86513964

# for veg_objekt in range(86512932, 86513964):
#   response = requests.get('https://www.vegvesen.no/nvdb/api/v2/vegobjekter/583/'+str(veg_objekt)).json()
#   for egenskap in response['egenskaper']:
#     if egenskap['navn']=='Kjørebanebredde':
#       pprint(egenskap['verdi'])


# 0_0 Grønn
# 2_2 Rødt
# 1_0 Blå
# 0_1 Blå?

class App(QMainWindow):

  def __init__(self):
    super().__init__()
    self.title = 'Nasjonal Vegdatabase'
    self.layout = QVBoxLayout()
    self.window = QWidget()
    self.initUI()

  def initUI(self):
    self.setWindowTitle(self.title)
    self.tabs = QTabWidget()

    # Create tabs
    self.vegkart_tab = QWidget()
    self.tekstbasert_tab = QWidget()
    self.tabs.addTab(self.vegkart_tab,"Vegkart")
    self.tabs.addTab(self.tekstbasert_tab,"Tekstbasert")
    self.vegkart_tab.layout = QVBoxLayout(self)
    self.tekstbasert_tab.layout = QVBoxLayout(self)

    # Vegbredde
    self.vegbredde_vegkart_label = QLabel('Vegbredde, totalt')
    self.vegbredde_tekstbasert_label = QLabel('Vegbredde, totalt')
    self.vegbredde_vegkart = QLineEdit(self)
    self.vegbredde_tekstbasert = QLineEdit(self)
    self.vegkart_tab.layout.addWidget(self.vegbredde_vegkart_label)
    self.vegkart_tab.layout.addWidget(self.vegbredde_vegkart)
    self.tekstbasert_tab.layout.addWidget(self.vegbredde_tekstbasert_label)
    self.tekstbasert_tab.layout.addWidget(self.vegbredde_tekstbasert)

    # Dekkebredde
    self.dekkebredde_vegkart_label = QLabel('Dekkebredde')
    self.dekkebredde_tekstbasert_label = QLabel('Dekkebredde')
    self.dekkebredde_vegkart = QLineEdit(self)
    self.dekkebredde_tekstbasert = QLineEdit(self)
    self.vegkart_tab.layout.addWidget(self.dekkebredde_vegkart_label)
    self.vegkart_tab.layout.addWidget(self.dekkebredde_vegkart)
    self.tekstbasert_tab.layout.addWidget(self.dekkebredde_tekstbasert_label)
    self.tekstbasert_tab.layout.addWidget(self.dekkebredde_tekstbasert)

    # Kjørebanebredde
    self.kjorebanebredde_vegkart_label = QLabel('Kjørebanebredde')
    self.kjorebanebredde_tekstbasert_label = QLabel('Kjørebanebredde')
    self.kjorebanebredde_vegkart = QLineEdit(self)
    self.kjorebanebredde_tekstbasert = QLineEdit(self)
    self.vegkart_tab.layout.addWidget(self.kjorebanebredde_vegkart_label)
    self.vegkart_tab.layout.addWidget(self.kjorebanebredde_vegkart)
    self.tekstbasert_tab.layout.addWidget(self.kjorebanebredde_tekstbasert_label)
    self.tekstbasert_tab.layout.addWidget(self.kjorebanebredde_tekstbasert)

    # Create a button in the window
    self.vegkart_button = QPushButton('Søk', self)
    self.tekstbasert_button = QPushButton('Søk', self)
    self.vegkart_tab.layout.addWidget(self.vegkart_button)
    self.tekstbasert_tab.layout.addWidget(self.tekstbasert_button)

    self.vegkart_tab.setLayout(self.vegkart_tab.layout)
    self.tekstbasert_tab.setLayout(self.tekstbasert_tab.layout)
    self.layout.addWidget(self.tabs)

    # Update Window
    self.window.setLayout(self.layout)
  
    # connect button to function on_click
    self.vegkart_button.clicked.connect(self.vegkart_button_click)
    self.tekstbasert_button.clicked.connect(self.tekstbasert_button_click)
    self.window.show()



  @pyqtSlot()
  def vegkart_button_click(self):
    vegbredde_value = self.vegbredde.text()
    #QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
    #self.textbox.setText("")
    base_url = "https://www.vegvesen.no/vegkart/vegkart/#kartlag:geodata"

    #todo:  add different type of roads to the url depending on what the user wrote
    #bug:   when adding a value to the input box, it will search correctly the first time,
    #       but not the second, the value will be blank in the browser filter bar
    vegbredde_totalt = 5264
    dekkebredde = 5555
    kjørebanebredde = 5556

    # cut the link into another piece, easier to change roadtype and other values
    edit_url = "/hva:(~(farge:'2_2,filter:(~(operator:'*3d,type_id:4566,verdi:(~5492)),(operator:'*3d,type_id:4568,verdi:(~18))),id:532),"
    type_url = "(farge:'0_1,filter:(~(operator:'*3e*3d,type_id:5555,verdi:(~"+str(vegbredde_value)+"))),id:583))"
    constant_url = "/hvor:(kommune:(~301,220,219,602,626))/@250164,6638305,9/vegobjekt:83641744:40a744:583"

    webbrowser.open(base_url+edit_url+type_url+constant_url)
  

  def tekstbasert_button_click(self):



if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = App()
  sys.exit(app.exec_())
