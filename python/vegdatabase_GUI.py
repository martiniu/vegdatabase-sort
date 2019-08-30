import json
import sys
import webbrowser
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class App(QMainWindow):

  def __init__(self):
    super().__init__()
    self.title = 'Nasjonal Vegdatabase'
    self.layout = QVBoxLayout()
    self.window = QWidget()

    with open('files/query_vegref_med_felt.json') as json_file:
      self.vegobjekter = json.load(json_file)

    self.initUI()


  def initUI(self):
    """
    Initializes various tabs, search-input, table and statistics.
    """
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
    self.tabell.setColumnCount(4)
    self.tabell.setHorizontalHeaderLabels(["Dekkebredde", "Diff. fra input", "Ant. felt", "Vegkartobjekt"])
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
    """
    This method returns a list of tuples where each tuple consist of key-value pair
    with unique "vegbreddeid" as key, and dictionary with "dekkebredde", "ant_felt" and "veglenkeid" as value. 
    """
    # This is python one-liner magic, if it does not make any sense to you, google "python list comprehension" and "python ternary operators"
    return [(key,value) for key,value in self.vegobjekter.items() if value['dekkebredde'] < int(self.tekstbasert_input_field.text())] \
      if str(self.tekstbasert_combo_box.currentText()) == '<' \
      else [(key,value) for key,value in self.vegobjekter.items() if value['dekkebredde'] >= int(self.tekstbasert_input_field.text())]


  def calculate_values(self):
    """
    This method sorts a filtered list of tuples, populates the table with correct values
    and updates the information screen after each search. 
    """
    filtered_values = self.filter_by_threshold()
    filtered_values = sorted(filtered_values, key=lambda i:i[1]['dekkebredde'])
    self.populate_table(filtered_values)

    if len(filtered_values) != 0:
      self.min_value = (min(filtered_values, key=lambda x:x[1]['dekkebredde']))[1]['dekkebredde']
      self.max_value = (max(filtered_values, key=lambda x:x[1]['dekkebredde']))[1]['dekkebredde']
      self.avg_value = sum([value[1]['dekkebredde'] for value in filtered_values])/len(filtered_values)
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
    """
    This method redirects a user to the vegkart with preconfigured inputs and search-values.
    """
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
    """
    This method populates the table with values. Values for each column are calculated and set in the correct cell.
    The last column consists of a button for each unique "vegbreddeid" and redirects user to the vegkart in order to inspect the "vegbredde" object. 
    """
    self.tabell.setRowCount(len(values))

    vegk_link = "https://www.vegvesen.no/nvdb/vegkart/v2/#kartlag:nib/hva:(~(farge:'2_2,filter:(~(operator:'*3d,type_id:4566,verdi:(~5492)),"
    vegk_link2 = "(operator:'*3d,type_id:4570,verdi:(~5506)),(operator:'*3d,type_id:4568,verdi:(~18))),id:532),"
    vegk_link3 = "(farge:'0_1,filter:(~(operator:'*3e*3d,type_id:5555,verdi:(~27))),id:583))/hvor:(fylke:(~3),"
    
    for row_number, row_data in enumerate(values):
      data = values[row_number]
      for col_number in range(4):
        if col_number == 0:
          self.tabell.setItem(row_number, col_number, QTableWidgetItem(str(data[1]['dekkebredde'])))
        elif col_number == 1:
          dekkebredde = float(data[1]['dekkebredde'])
          diff = round(dekkebredde-float(self.tekstbasert_input_field.text()),1)
          self.tabell.setItem(row_number, col_number, QTableWidgetItem(str(diff)))
        elif col_number == 2:
          self.tabell.setItem(row_number, col_number, QTableWidgetItem(str(data[1]['ant_felt'])))
        elif col_number == 3:
          vegkart_objectid_button = QPushButton('Søk', self)
          vegkart_objectid_button.clicked.connect(lambda checked, arg=data[0]: webbrowser.open(vegk_link+vegk_link2+vegk_link3+"kommune:(~602,626,219,220))/@261273,6645269,8/vegobjekt:"+str(arg)+":40a744:583"))
          self.tabell.setCellWidget(row_number, col_number, vegkart_objectid_button)


if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = App()
  sys.exit(app.exec_())