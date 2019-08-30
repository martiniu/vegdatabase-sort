import requests
import json
import sys
from pprint import pprint
import webbrowser
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import Qt


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
    QAbstractTableModel.__init__(self, parent=None)
    self.title = 'Nasjonal Vegdatabase'
    self.layout = QVBoxLayout()
    self.window = QWidget()

    with open('files/query_vegref_med_felt.json') as json_file:
      self.vegobjekter = json.load(json_file)

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

    # Vegkart search layout
    self.vegkart_label1 = QLabel('Søk etter Dekkebredde som er')
    self.vegkart_label2 = QLabel('enn')
    self.vegkart_combo_box = QComboBox(self)
    self.vegkart_combo_box.addItem('>=')
    self.vegkart_combo_box.addItem('<')
    self.vegkart_input_field = QLineEdit(self)
    self.vegkart_search_button = QPushButton('Søk', self)

    # Tekstbasert search layout
    self.tekstbasert_label1 = QLabel('Søk etter Dekkebredde som er')
    self.tekstbasert_label2 = QLabel('enn')
    self.tekstbasert_combo_box = QComboBox(self)
    self.tekstbasert_combo_box.addItem('>=')
    self.tekstbasert_combo_box.addItem('<')
    self.tekstbasert_input_field = QLineEdit(self)
    self.tekstbasert_search_button = QPushButton('Søk', self)

    # Vegkart search layout assembled
    self.vegkart_description_layout = QHBoxLayout()
    self.vegkart_description_layout.addWidget(self.vegkart_label1)
    self.vegkart_description_layout.addWidget(self.vegkart_combo_box)
    self.vegkart_description_layout.addWidget(self.vegkart_label2)
    self.vegkart_description_layout.addWidget(self.vegkart_input_field)
    self.vegkart_description_layout.addWidget(self.vegkart_search_button)
    self.vegkart_tab.layout.addLayout(self.vegkart_description_layout)

    # Tekstbasert search layout assembled
    self.tekstbasert_description_layout = QHBoxLayout()
    self.tekstbasert_description_layout.addWidget(self.tekstbasert_label1)
    self.tekstbasert_description_layout.addWidget(self.tekstbasert_combo_box)
    self.tekstbasert_description_layout.addWidget(self.tekstbasert_label2)
    self.tekstbasert_description_layout.addWidget(self.tekstbasert_input_field)
    self.tekstbasert_description_layout.addWidget(self.tekstbasert_search_button)
    self.tekstbasert_tab.layout.addLayout(self.tekstbasert_description_layout)

    # Infotable
    self.tabell = QTableWidget()
    self.tabell.setColumnCount(3)
    self.tabell.setHorizontalHeaderLabels(["Dekkebredde", "Diff. fra input", "Ant. felt"])
    self.tekstbasert_tab.layout.addWidget(self.tabell)

    # Infoscreen
    self.info_label_min = QLabel('Min: \t 0 \t (Minste dekkebredde)')
    self.info_label_max = QLabel('Max: \t 0 \t (Største dekkebredde)')
    self.info_label_avg = QLabel('Avg: \t 0 \t (Gjennomsnittsbredde)')
    self.info_label_over = QLabel('%> \t 0 \t (% av resultatet som er større enn inputsverdi)')
    self.info_label_under = QLabel('%< \t 0 \t (% av resultatet som er mindre enn inputsverdi)')

    # Updating tabs layout
    self.tekstbasert_tab.layout.addWidget(self.info_label_min)
    self.tekstbasert_tab.layout.addWidget(self.info_label_max)
    self.tekstbasert_tab.layout.addWidget(self.info_label_avg)
    self.tekstbasert_tab.layout.addWidget(self.info_label_over)
    self.tekstbasert_tab.layout.addWidget(self.info_label_under)
    self.tekstbasert_tab.setLayout(self.tekstbasert_tab.layout)
    self.vegkart_tab.setLayout(self.vegkart_tab.layout)
    self.layout.addWidget(self.tabs)
    self.window.setLayout(self.layout)

    # Connect buttons to functions
    self.tekstbasert_search_button.clicked.connect(self.calculate_values)
    self.vegkart_search_button.clicked.connect(self.vegkart_button_click)
    # Show GUI
    self.window.show()


  def filter_by_threshold(self):
    # This is python one-liner magic, if it does not make any sense to you, google "python list comprehension" and "python ternary operators"
    return [value for key,value in self.vegobjekter.items() if value['dekkebredde'] < int(self.tekstbasert_input_field.text())] \
      if str(self.tekstbasert_combo_box.currentText()) == '<' \
      else [value for key,value in self.vegobjekter.items() if value['dekkebredde'] >= int(self.tekstbasert_input_field.text())]

  def calculate_values(self):
    filtered_values = self.filter_by_threshold()
    filtered_values = sorted(filtered_values, key=lambda i:i['dekkebredde'], reverse=False)
    self.populate_table(filtered_values)

    if len(filtered_values) != 0:
      self.min_value = (min(filtered_values, key=lambda x:x['dekkebredde']))['dekkebredde']
      self.max_value = (max(filtered_values, key=lambda x:x['dekkebredde']))['dekkebredde']
      self.avg_value = sum([value['dekkebredde'] for value in filtered_values])/len(filtered_values)
    else:
      self.min_value, self.max_value, self.avg_value = 0,0,0

    if str(self.tekstbasert_combo_box.currentText()) == '<':
      self.under_value = round(len(filtered_values)/len(self.vegobjekter)*100,1)
      self.over_value = round(100 - self.under_value,1)
    else:
      self.over_value = round(len(filtered_values)/len(self.vegobjekter)*100,1)
      self.under_value = round(100 - self.over_value,1)

    self.info_label_min.setText('Min: \t'+str(self.min_value)+'\t (Minste dekkebredde)')
    self.info_label_max.setText('Max: \t'+str(self.max_value)+'\t (Største dekkebredde)')
    self.info_label_avg.setText('Avg: \t'+str(round(self.avg_value,1))+'\t (Gjennomsnittsbredde)')
    self.info_label_over.setText('%> \t'+str(self.over_value)+'\t (% av resultatet som er større enn inputsverdi)')
    self.info_label_under.setText('%< \t'+str(self.under_value)+'\t (% av resultatet som er mindre enn inputsverdi)')


  def vegkart_button_click(self):
    dekkebredde_value = self.vegkart_input_field.text()
    base_url = "https://www.vegvesen.no/nvdb/vegkart/v2/#kartlag:geodata"
    edit_url, edit_url2, edit_url3 = "","",""

    if str(self.vegkart_combo_box.currentText()) == '<':
      edit_url = "/hva:(~(farge:'2_2,filter:(~(operator:'*3d,type_id:4566,verdi:(~5492)),(operator:'*3d,type_id:4570,verdi:(~5506)),"
      edit_url2 = "(operator:'*3d,type_id:4568,verdi:(~18))),id:532),(farge:'0_1,filter:(~(operator:'*3c,type_id:5555,verdi:(~"+str(dekkebredde_value)+"))),id:583))"
      edit_url3 = "/hvor:(fylke:(~3),kommune:(~602,626,219,220))/@253703,6648215,12"
    else:
      edit_url = "/hva:(~(farge:'2_2,filter:(~(operator:'*3d,type_id:4566,verdi:(~5492)),(operator:'*3d,type_id:4570,verdi:(~5506)),"
      edit_url2 = "(operator:'*3d,type_id:4568,verdi:(~18))),id:532),(farge:'0_1,filter:(~(operator:'*3e*3d,type_id:5555,verdi:(~"+str(dekkebredde_value)+"))),id:583))"
      edit_url3 = "/hvor:(fylke:(~3),kommune:(~602,626,219,220))/@253703,6648215,12"

    self.tekstbasert_input_field.setText(dekkebredde_value)
    self.tekstbasert_combo_box.setCurrentText(self.vegkart_combo_box.currentText())
    self.calculate_values()
    webbrowser.open(base_url+edit_url+edit_url2+edit_url3)


  def populate_table(self, values):
    self.tabell.setRowCount(len(values))
    for row_number, row_data in enumerate(values):
      for col_number, data in enumerate(row_data):
        if data=='dekkebredde':
          self.tabell.setItem(row_number, col_number, QTableWidgetItem(str(values[row_number][data])))
        elif data=='ant_felt':
          self.tabell.setItem(row_number, col_number, QTableWidgetItem(str(values[row_number][data])))
        else:
          dekkebredde = float(values[row_number]['dekkebredde'])
          diff = round(dekkebredde-float(self.tekstbasert_input_field.text()),1)
          self.tabell.setItem(row_number, col_number, QTableWidgetItem(str(diff)))

if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = App()
  sys.exit(app.exec_())
