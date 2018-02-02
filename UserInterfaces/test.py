# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 11:21:29 2014

@author: danie_000
"""

import sys, time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import networkx as nx
import pylab as pl
import matplotlib.pyplot as plt
#import interdependency_analysis_v5_0_1 as res 
import random as r
#import interdependency_analysis_v5_2_9 as res 
#import inhouse_algorithms as customnets
#import visalgorithms_v10_1 as vis
#import metric_calcs_v_1_0 as mc
#import options_window_v1_0_1 as ow

class DbConnect(QDialog):  
#class DbConnect(QMainWindow):
    '''Class for the database parameters connection window.'''
    def __init__(self, parent=None):
        #super(dbconnect, self).__init__(parent)
        QDialog.__init__(self, parent)   
        
        #parametes for database connection               
        exitAction = QAction('&Exit',self)
        exitAction.triggered.connect(qApp.quit)
        '''
        openAction = QAction('&Open',self)
        openAction.triggered.connect(self.openfile)               
        
        saveAction = QAction('&Save', self)
        saveAction.triggered.connect(self.savefile) 
        
        menubar=self.menuBar() #create menu bar
        fileMenu = menubar.addMenu('&File') #add file menu
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)
        '''
        lbl1 = QLabel('dbname: ', self)
        lbl1.move(25,30)
        lbl1.adjustSize()
        self.txtinput1 = QLineEdit(self)        
        self.txtinput1.move(75, 25)
        self.txtinput1.setToolTip('name of database')
        lbl2 = QLabel('host: ', self)
        lbl2.move(25,55)
        lbl2.adjustSize()
        self.txtinput2 = QLineEdit(self)        
        self.txtinput2.move(75, 50)
        self.txtinput2.setToolTip('host of database')
        lbl3 = QLabel('port: ', self)
        lbl3.move(25,80)
        lbl3.adjustSize()        
        self.txtinput3 = QLineEdit(self)        
        self.txtinput3.move(75, 75)
        self.txtinput3.setToolTip('port')
        lbl4 = QLabel('user: ', self)
        lbl4.move(25,105)
        lbl4.adjustSize()
        self.txtinput4 = QLineEdit(self)        
        self.txtinput4.move(75, 100)
        self.txtinput4.setToolTip('user')
        lbl5 = QLabel('password: ', self)
        lbl5.move(25,130)
        lbl5.adjustSize()
        self.txtinput5 = QLineEdit(self)        
        self.txtinput5.move(75, 125)
        self.txtinput5.setToolTip('password')
        lbl6 = QLabel('net name: ', self)
        lbl6.move(25,160)
        lbl6.adjustSize()
        self.txtinput6 = QLineEdit(self)        
        self.txtinput6.move(75, 155)
        self.txtinput6.setToolTip('network name in database')

        self.clearbtn = QPushButton('Clear', self)
        self.clearbtn.setToolTip('Clear all input boxes')
        self.clearbtn.move(10, 185)
        self.clearbtn.adjustSize()
        self.clearbtn.clicked.connect(self.clear)
        
        self.openbtn = QPushButton('Open', self)
        self.openbtn.setToolTip('Open a text file storing connection parameters')
        self.openbtn.move(90, 185)
        self.openbtn.adjustSize()
        self.openbtn.clicked.connect(self.openfile)
        
        self.savebtn = QPushButton('Save', self)
        self.savebtn.setToolTip('Save the connection parameters to a text file')
        self.savebtn.move(170, 185)
        self.savebtn.adjustSize()
        self.savebtn.clicked.connect(self.savefile)

        self.applybtn = QPushButton('Apply', self)
        self.applybtn.setToolTip('Connect to the database and run the analysis')
        self.applybtn.move(170, 215)
        self.applybtn.adjustSize()
        self.applybtn.clicked.connect(self.applyclick)
        
        self.cancelbtn = QPushButton('Cancel', self)
        self.cancelbtn.setToolTip('Cancel the analysis and close the window')
        self.cancelbtn.move(10, 215)
        self.cancelbtn.adjustSize()
        self.cancelbtn.clicked.connect(self.cancel)
             
        self.restore = QPushButton('Restore', self)
        self.restore.setToolTip('Restore the settings from the previous successful analyiss this session')
        self.restore.move(90, 215)
        self.restore.adjustSize()
        self.restore.clicked.connect(self.restoreinputs)
        #get the last set of connection parameters if they exist is not all will be None
        self.dbconnect = self.pullindbconnect()
        DBNAME,HOST,PORT,USER,PASSWORD,NETNAME=self.dbconnect
        if HOST == None and DBNAME == None and USER == None and NETNAME == None and PORT == None and PASSWORD == None:
            self.restore.setEnabled(False)

        self.setGeometry(300,500,250,250)#above; vertical place on screen, hoz place on screen, width of window, height of window
        self.setWindowTitle('db Connection Parameters')  #title of windpw
        self.setWindowIcon(QIcon('logo.png'))
        self.show()#show window   
        
    def openfile(self):
        '''Opens a text file for the user to load in a set of connection 
        parameters. Needs some error checking to make stable though.'''
        fname = QFileDialog.getOpenFileName(self, 'Open file')
        if fname == '': #if the user closes the window or in case the file is read only
            return
        text=open(fname).read()
        text = text.split('\n')
        self.dbconnect = []
        for line in text:
            parameter, txtinput = line.split(';')
            self.dbconnect.append(txtinput)
        self.txtinput1.setText(self.dbconnect[0])
        self.txtinput2.setText(self.dbconnect[1])
        self.txtinput3.setText(self.dbconnect[2])
        self.txtinput4.setText(self.dbconnect[3])
        self.txtinput5.setText(self.dbconnect[4])   
        self.txtinput6.setText(self.dbconnect[5])
            
    def savefile(self):
        '''Function for saving the parameters in a text file for future use. 
        Called by the 'Save' button only.'''
        DBNAME,HOST,PORT,USER,PASSWORD,NETNAME=self.dbconnect
        fname = QFileDialog.getSaveFileName(self, 'Save File', '.txt')
        if fname == '': #if the user closes the window or in case the file is read only
            return
        f = open(fname,'a')
        f.write('DBNAME;%s\nHOST;%s\nPORT;%s\nUSER;%s\nPASSWORD;%s\nNETNAME;%s' %(DBNAME, HOST, PORT,USER, PASSWORD, NETNAME))
        f.close()

    def clear(self):
        '''Clears all six input boxes. Called by the 'Clear' button.'''
        self.txtinput1.setText('')
        self.txtinput2.setText('')
        self.txtinput3.setText('')
        self.txtinput4.setText('')
        self.txtinput5.setText('')        
        self.txtinput6.setText('')
        
    def pullindbconnect(self):
        '''This pulls in the database connection properties from the main 
        window.'''
        dbconnect = window.updatedb_db()
        return dbconnect
   
    def applyclick(self):
        '''Save the text from that was in the text boxes when function called.'''
        self.DBNAME = self.txtinput1.text()
        self.HOST = self.txtinput2.text()
        self.PORT = self.txtinput3.text()
        self.USER = self.txtinput4.text()
        self.PASSWORD = self.txtinput5.text()        
        self.NETNAME = self.txtinput6.text()
        
        try:
            #needed to convert the items to strings for the connection
            self.DBNAME = str(self.DBNAME)
            self.HOST = str(self.HOST)
            self.PORT = str(self.PORT)
            self.USER = str(self.USER)
            self.PASSWORD = str(self.PASSWORD)
            self.NETNAME = str(self.NETNAME)              
            '''
            # paramers for a safe conenction that should always work
            self.DBNAME = 'roads_national'
            self.HOST = 'localhost'
            self.PORT = '5433'
            self.USER = 'postgres'
            self.PASSWORD = 'aaSD2011'
            '''
            conn = None
            conn = ogr.Open("PG: host='%s' dbname='%s' user='%s' password='%s' port='%s'" % (self.HOST, self.DBNAME, self.USER, self.PASSWORD, self.PORT))
            conn_worked = True
        except:
            QMessageBox.warning(self, 'Error!', "Could not connect to the database. Please check your inputs and try again.",'&OK')
            self.G = None
            conn_worked = False
            return
            
        if conn_worked == True:
            try:
                self.NETNAME = str(self.NETNAME)
                '''                
                #this is part of the known set for testing
                self.NETNAME = 'ire_m_t_roads' 
                '''
                self.G = nx_pgnet.read(conn).pgnet(self.NETNAME)
                #package the successfult connection parameters
                self.dbconnect = self.DBNAME, self.HOST, self.PORT, self.USER, self.PASSWORD, self.NETNAME
            except:
                QMessageBox.warning(self, 'Error!', "Could not find network in database. Please check the network name.",'&OK')             
                return
        
        #return the good set of connection parameters and the graph
        window.updateGUI_db(self.dbconnect, self.G)
        self.close()
    
    def cancel(self):
        '''Clear the text boxes and close the window when the cancel button is 
        clicked.'''
        self.close()
        
    def getval(self):
        '''Used to pass the database connection data back to the window class.'''
        return self.DBNAME, self.HOST, self.PORT, self.USER, self.PASSWORD, self.NETNAME
    
    def restoreinputs(self, dbconnect):
        '''Restore the previusoly saved vlaues from the last successful 
        execution of the database connection. Data is retireved from a global 
        variable.'''
        DBNAME,HOST,PORT,USER,PASSWORD,NETNAME=self.dbconnect
        if HOST == None and DBNAME == None and USER == None and NETNAME == None and PORT == None and PASSWORD == None:
            #when no inputs have been used suceesfully yet
            QMessageBox.warning(self, 'Warning', "No inputs to restore. Inputs must have been used already before they can be restored." , '&OK')
        else:
            self.DBNAME, self.HOST, self.PORT, self.USER, self.PASSWORD, self.NETNAME = self.dbconnect
            self.txtinput1.setText(self.DBNAME)
            self.txtinput2.setText(self.HOST)
            self.txtinput3.setText(self.PORT)
            self.txtinput4.setText(self.USER)
            self.txtinput5.setText(self.PASSWORD)         
            self.txtinput6.setText(self.NETNAME)
            
class Window(QMainWindow):
    def __init__(self, parent = None):
        QWidget.__init__(self,parent)        
        
        self.setGeometry(300,300,600,300)
        self.setWindowTitle(Gene)        
        
        
        # Create actions        
        
        exitAction = QAction('&Exit',self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        #exitAction.triggered.connect(self.closeall)
        
        resetAction = QAction('&Reset Parameters', self)
        resetAction.setStatusTip('Reset Parameters')
        resetAction.triggered.connect(self.reset)
         
        # create a menu bar with file, edit menus 
        self.statusBar()
        menubar  = self.menuBar()
        fileMenu = menubar.addMenu('&File') # add file menu
        editMenu = menubar.addMenu('&Edit') # add edit menu
                
        
        
        # add actions to file menu
        fileMenu.addAction(exitAction)
        
        # add actions to edit menu
        editMenu.addAction(resetAction)
        
        
        def reset(self):
            return 1
            
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
        