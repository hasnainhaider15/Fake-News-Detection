#editor minimap is disabled

import sys
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication, QDialog, QMessageBox, QWidget
from PyQt5.QtCore import QAbstractTableModel, Qt
from firebasedatabase import DatabaseModel
from datashow import pandasModel
import pandas as pd
from PIL import Image
import pytesseract
from fuzzywuzzy import process, fuzz

uifile_1 = 'login.ui'
form_1, base_1 = uic.loadUiType(uifile_1)

uifile_2 = 'register.ui'
form_2, base_2 = uic.loadUiType(uifile_2)

uifile_3 = "chose.ui"
form_3, base_3 = uic.loadUiType(uifile_3)

uifile_4 = "reset.ui"
form_4, base_4 = uic.loadUiType(uifile_4)

uifile_5 = "textdetect.ui"
form_5, base_5 = uic.loadUiType(uifile_5)

uifile_6 = "ocr.ui"
form_6, base_6 = uic.loadUiType(uifile_6)

"""Login Form"""

class MyLogin(base_1, form_1):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.login_password.setEchoMode(QtWidgets.QLineEdit.Password)

        """Login page Button click events"""
        self.register_button.clicked.connect(self.myRegisterwindow)
        self.login_button.clicked.connect(self.loginDetails)
        self.forget_button.clicked.connect(self.myresetwindow)
        self.guest_button.clicked.connect(self.mychosewindow)
    
    def loginDetails(self):
        self.username = self.login_username.text().strip()
        self.password = self.login_password.text().strip()
        self.name = ''
        if len(self.username)== 0:
            errorpopup("Username cannot be left blank")
        elif len(self.password) == 0:
            errorpopup("Password cannot be left blank")
        else:
            self.loginQuery()

    def loginQuery(self):
        data = DatabaseModel(self.name, self.username, self.password)
        result = data.login()
        if type(result) == dict:
            self.clearAll()
            self.mychosewindow()
        else:
            errorpopup(result)
            

    """Success popup"""

    def successpopup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Success")
        msg.setText("Successfull")
        msg.exec_()

    """Clearing all textboxes"""

    def clearAll(self):
        fields = [self.login_username, self.login_password]
        for field in fields:
            field.clear()

    def myRegisterwindow(self):
        self.close()
        self.child_win = MyRegister(self)
        self.child_win.show()
        
    def mychosewindow(self):
        self.close()
        self.chosewindow = MyChose()
        self.chosewindow.show()
        
    def myresetwindow(self):
        self.close()
        self.resetwindow = MyReset()
        self.resetwindow.show()

"""Registeration Form"""
class MyRegister(base_2, form_2):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.register_password.setEchoMode(QtWidgets.QLineEdit.Password)
        
        """Button Clicked Events"""
        self.go_back_button.clicked.connect(self.loginclass)
        self.register_button.clicked.connect(self.details)

    """Pasing text to variable/ appliting checks/calling db method"""
    def details(self):
        
        self.name = self.register_name.text()
        
        self.username = self.register_username.text()
        self.password = self.register_password.text()
        if len(self.name) == 0:
            errorpopup("Name field cannot be empty")
        elif len(self.password)==0:
            errorpopup("Password field cannot be empty")
        elif len(self.username)== 0:
            errorpopup("Username field cannot be empty")
        else:
            self.registerquery()

    """Calling databade to register user"""
    def registerquery(self):
        data = DatabaseModel(self.name, self.username, self.password)
        data = data.register()
        if type(data) == dict:
            self.clearAll()
            self.successpopup()
        else:
            errorpopup(data)

    """Success popup"""
    def successpopup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Success")
        msg.setText("Registeration Successfull")
        msg.exec_()

    """Clearing all textboxes"""
    def clearAll(self):
        fields = [self.register_name,
                  self.register_username, self.register_password]
        for field in fields:
            field.clear()

    """Instance of Login class to move back to Login page"""
    def loginclass(self):
        self.close()
        self.loginwindow = MyLogin()
        self.loginwindow.show()

"""Password Reset"""
class MyReset(base_4, form_4):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        """Button CLicked Events"""
        self.send_button.clicked.connect(self.restdetails)
        self.go_back_button.clicked.connect(self.loginclasschose)

    """Geting details from textbox and validation check"""
    def restdetails(self):
        self.reset = self.forget_textbox.text()
        self.a = ''
        self.b = ''
        if len(self.reset) == 0:
            errorpopup("Field cannot be left blank")
        else:
            self.sendrestemail()
    """Use database script to sent password reset email"""
    def sendrestemail(self):
        data = DatabaseModel(self.a, self.reset, self.b)
        resetEmail = data.paswordReset()
        if type(resetEmail) == dict:
            self.forget_textbox.clear()
            self.successpopup() 
        else:
            errorpopup(resetEmail)

    """Success popup window"""       
    def successpopup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Success")
        text = "Email has been sent to: " + self.reset
        msg.setText(text)
        msg.exec_()

    """Login class instance to move back to login class"""
    def loginclasschose(self):
        self.close()
        self.loginwindow = MyLogin()
        self.loginwindow.show()

"""Chose page"""
class MyChose(base_3, form_3):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        """Button CLick Events"""
        self.logout_button.clicked.connect(self.loginclasschose)
        self.image_option_button.clicked.connect(self.imageOptionWindow)
        self.text_option_button.clicked.connect(self.textOptionWindow)
    """Instance of login class"""
    def loginclasschose(self):
        self.close()
        self.loginwindow = MyLogin()
        self.loginwindow.show()

    """Instance of OCR/ImageDetection Class"""
    def imageOptionWindow(self):
        self.close()
        self.textdetection = ImageDetection()
        self.textdetection.show()

    """Instance of Text Detection Class"""
    def textOptionWindow(self):
        self.close()
        self.textdetection = TextDetection()
        self.textdetection.show()

"""Detection through Text"""
class TextDetection(base_5, form_5):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.limit.addItems(
            ['1', '2', '3', '4'])
        self.select_algo.addItems(
            ["token_sort_ratio", "partial_ratio", "ratio"])

        self.geting_data()

        """BUtton Click Events"""
        self.go_back_button.clicked.connect(self.textchoicewindow)
        self.search_button.clicked.connect(self.text_details)
    
    """"Check to give warning on empty path"""
    def text_details(self):
        self.text_paths = self.text_path.text()
        if len(self.text_paths) == 0:
            errorpopup("Kindly type text for better results. Thanks!")
        else:
            self.get_matches()

    """Loading dataset"""
    def geting_data(self):
        try:
            self.df = pd.read_csv("newdata.csv")
            self.filt = self.df['News'] == '0'
            self.df.drop(index=self.df[self.filt].index, inplace=True)
            self.choices = self.df['News'].unique()
            
        except FileNotFoundError:
           errorpopup("Dataset was not found")

    """Sequence Matcher Algoritim"""
    def get_matches(self):
        self.algo = self.select_algo.currentIndex()
        if self.algo == 0:
            self.algo = fuzz.token_sort_ratio
        elif self.algo == 1:
            self.algo =  fuzz.partial_ratio
        elif self.algo == 2:
            self.algo = fuzz.ratio

        self.limits = self.limit.currentText()
        self.limits = int(self.limits)
        self.results = process.extract(self.text_paths, self.choices, limit=self.limits, scorer=self.algo)
        self.option()
    
    """Displaying Results"""
    def option(self, role = Qt.DisplayRole):
        query = []
        score = []
        for i in self.results:
            query.append(i[0])
            score.append(i[1])

        authen = categories(score)
        df = pd.DataFrame({'Mactching Queries': query,
                            'Score': score,
                            'Authenticity': authen})
        
        datatable = pandasModel(df)
        self.table.setModel(datatable)
        
    """Instance of Choice Window / Clicking goback button"""
    def textchoicewindow(self):
        self.close()
        self.chosewindow = MyChose()
        self.chosewindow.show()

"""Detection through Image"""
class ImageDetection(base_6, form_6):
    def __init__(self):
        super(base_6, self).__init__()
        self.setupUi(self)
        self.limit.addItems(
            ['1', '2', '3', '4'])
        self.select_algo.addItems(
            ["token_sort_ratio", "partial_ratio", "ratio"])
        self.geting_data()
        self.go_back_button.clicked.connect(self.imagechoicewindow)
        self.browse_button.clicked.connect(self.browseImage)

    """Browsing Image"""
    def browseImage(self):
        self.fname = QFileDialog.getOpenFileName(
            self, 'Open File', 'c\\', 'Image files (*.jpg *.png)')
        self.path = self.fname[0]
        self.image_path.setText(self.path)
        self.search_button.clicked.connect(self.checkpathtext)
    
    """Checking path if it has text than it runs otherwise give alert"""
    def checkpathtext(self):
        if len(self.path) == 0:
            errorpopup("Path is blank! Browse first")
        else:
            
            self.convert_image_to_text()

    """OCR Algorithim"""
    def convert_image_to_text(self):
        pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
        self.im = Image.open(self.path)
        self.text = pytesseract.image_to_string(self.im, lang='eng')
        self.get_matches()

    """Loading dataset"""
    def geting_data(self):
        try:
            self.df = pd.read_csv("newdata.csv")
            self.filt = self.df['News'] == '0'
            self.df.drop(index=self.df[self.filt].index, inplace=True)
            self.choices = self.df['News'].unique()
        except FileNotFoundError:
            print("Dataset was not found")

    """Custom matches for user choices and Algorithim for String Sequence Matcher"""
    def get_matches(self):
        self.algo = self.select_algo.currentIndex()
        if self.algo == 0:
            self.algo = fuzz.token_sort_ratio
        elif self.algo == 1:
            self.algo = fuzz.partial_ratio
        elif self.algo == 2:
            self.algo = fuzz.ratio
        self.limits = self.limit.currentText()
        self.limits = int(self.limits)
        self.results = process.extract(
            self.text, self.choices, limit=self.limits, scorer=self.algo)
        self.option()

    """Displaying data in table view"""
    def option(self, role=Qt.DisplayRole):
        query = []
        score = []
        for i in self.results:
            query.append(i[0])
            score.append(i[1])
        
        authen = categories(score)
        df = pd.DataFrame({'Mactching Queries': query,
                           'Score': score,
                           'Authenticity': authen})

        datatable = pandasModel(df)
        self.table.setModel(datatable)
   
    """Instance of Choice Window / Clicking goback button"""
    def imagechoicewindow(self):
        self.close()
        self.chosewindow = MyChose()
        self.chosewindow.show()

"""Gernal perpouse popup DialogBox"""
def errorpopup(data):
    msg = QMessageBox()
    msg.setWindowTitle("Error")
    msg.setText(data)
    msg.exec_()

"""Comparing score to display Real/Fake"""
def categories(data):
    fake = []
    for i in data:
        if i <= 100 and i > 85:
            fake.append("Real")
        elif i <= 85 and i > 75:
            fake.append(("Mostly Real"))
        elif i <= 75 and i > 65:
            fake.append("Mostly Fake")
        elif i <= 65:
            fake.append("Fake")
    return fake


"""Script Enters through here"""
if __name__ == "__main__":
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    window = MyLogin()
    window.show()
    sys.exit(app.exec_())
