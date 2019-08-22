import requests
import json
import sys
from pprint import pprint
import webbrowser
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QMainWindow, QMessageBox, QLabel
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
# 0_1 Blå?@

class App(QMainWindow):

  def __init__(self):
    super().__init__()
    self.title = 'PyQt5 textbox - pythonspot.com'
    self.layout = QVBoxLayout()
    self.window = QWidget()
    self.initUI()

  def initUI(self):
    self.setWindowTitle(self.title)
    #self.setGeometry(self.left, self.top, self.width, self.height)

    # Vegbredde
    self.vegbredde_label = QLabel('Vegbredde, totalt')
    self.vegbredde = QLineEdit(self)
    self.layout.addWidget(self.vegbredde_label)
    self.layout.addWidget(self.vegbredde)

    # Dekkebredde
    self.dekkebredde_label = QLabel('Dekkebredde')
    self.dekkebredde = QLineEdit(self)
    self.layout.addWidget(self.dekkebredde_label)
    self.layout.addWidget(self.dekkebredde)

    # Kjørebanebredde
    self.kjorebanebredde_label = QLabel('Kjørebanebredde')
    self.kjorebanebredde = QLineEdit(self)
    self.layout.addWidget(self.kjorebanebredde_label)
    self.layout.addWidget(self.kjorebanebredde)

    # Create a button in the window
    self.button = QPushButton('Søk', self)
    self.layout.addWidget(self.button)

    # Update Window
    self.window.setLayout(self.layout)

    # connect button to function on_click
    self.button.clicked.connect(self.on_click)
    self.window.show()

  @pyqtSlot()
  def on_click(self):
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


if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = App()
  sys.exit(app.exec_())

# app = QApplication([])
# window = QWidget()

# asd = QLineEdit()
# layout.addWidget(asd)
# layout.addWidget(QPushButton('Top'))
# layout.addWidget(QPushButton('Bottom'))
# window.setLayout(layout)
# window.show()

# print(asd.text())



#dekkebredde = input("Dekkebredde større enn: ")


#app.exec_()
