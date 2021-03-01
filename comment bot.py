import requests,os,threading,sys,uuid,time

from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5.QtWidgets import *

from PyQt5 import QtWidgets,QtGui
from PyQt5.QtGui import *
from PyQt5.uic import loadUi

from main import *

class Main(QDialog,Ui_Dialog):
    def __init__(self,parent=None):
        super(Main,self).__init__(parent)
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Comment bot @h.cz_")

        self.uid = str(uuid.uuid4())
        self.r = requests.session()


        self.done = 0
        self.false = 0
        self.error = 0
        
        self.tabWidget.tabBar().setVisible(False)

        self.login_button.clicked.connect(self.login)

        self.start_button.clicked.connect(self.start)

        self.ff = False 
    def login(self):
        
        self.header = {
            'User-Agent': "Instagram 151.0.0.23.120 Android (26/8.0.0; 480dpi; 1080x1920; samsung; SM-G930T; heroqltetmo; qcom; ar_AE; 232867993)",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US",
            "X-IG-Capabilities": "3brTvw==",
            "X-IG-Connection-Type": "WIFI",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            'Host': 'i.instagram.com'
        }
        dat = {
            '_uuid': self.uid,
            'username': self.username.text(),
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:1589682409:{self.password.text()}',
            'queryParams': '{}',
            'optIntoOneTap': 'false',
            'device_id': self.uid,
            'from_reg': 'false',
            '_csrftoken': 'missing',
            'login_attempt_count': '0'
        }
        url = "https://i.instagram.com/api/v1/accounts/login/"

        self.res = self.r.post(url,data=dat,headers=self.header)
        if ('"logged_in_user"') in self.res.text:
            print("login done")
            self.tabWidget.setCurrentIndex(1)
            
        elif ("Incorrect Username") in self.res.text:
            
            usererror = QMessageBox()
            usererror.setText("Check your Username")
            usererror.setIcon(QMessageBox.Critical)
            x = usererror.exec_()
        elif ('Incorrect password') in self.res.text:
            
            passerror = QMessageBox()
            passerror.setWindowTitle("")
            passerror.setText("Check your Password")
            passerror.setIcon(QMessageBox.Critical)
            x = passerror.exec_()
        elif ('checkpoint_challenge_required') in self.res.text:
            
            secerror = QMessageBox()
            secerror.setText("Secure !")
            secerror.setIcon(QMessageBox.Warning)
            x = secerror.exec_()
        else:
            
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setText("ERORRRRRRRR")
            x = error.exec_()
        
    def get_id(self):
        
        url = str(self.url.text()) + '?__a=1'
        respon = self.r.get(url).json()
        id = respon['graphql']['shortcode_media']['id']
        print(id)
        return id
        
    def commentt(self):
        url = f"https://i.instagram.com/api/v1/media/{self._id}/comment/"
        data = {
            "_csrftoken":"missing",
            "_uid": self.uid,
            "_uuid":self.uid,
            "comment_text": self.comment.text(),
            "is_carousel_bumped_post":"false",
            "container_module":"comments_v2_feed_timeline",
            "feed_position":"0"
        }
        while True:
            respon = self.r.post(url,data=data,headers=self.header)
            
            if ('"status": "ok"') in respon.text:
                
                self.done += 1
                self.done_com.setText(str(self.done))
            if ('"status": "fail"') in respon.text:
                
                self.false += 1
                self.false_com.setText(str(self.false))
            else:
                pass
            time.sleep(int(self.sleep.text()))
    
    def start(self):
        if self.ff == False:
            self._id = self.get_id()
            print(self.url.text())
            threading.Thread(target=self.commentt).start()
            self.ff = True
        else:
            print("fgfsgf")
        



            
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = Main()
    widget.show()
    sys.exit(app.exec())