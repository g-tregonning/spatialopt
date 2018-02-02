# -*- coding: utf-8 -*-
"""
Genetic Algorithm Tool v1
@author Daniel Caparros-Midwood


GUI to input the parameters for the genetic algorithm operation.
Optimising the location of residential development over London

GUI provides input boxes for parameters for the search

Ideas:
    - Could have a processing screen which appears:
        @ Best performance in each iteration (max or min)
        @ time elapsed
        @ num of solutions evaluated
        @ 


"""

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class GUIConnect(QDialog):
    """Class for the Genetic Algorithm parameters window"""
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        
        exitAction = QAction('&Exit', self)
        exitAction.triggered.connect(qApp.quit)



class Window(QMainWindow):
    def __init__(self, parent = None):
        QWidget.__init__(self,parent)        
        
        self.setGeometry(300,300,600,300)
        self.setWindowTitle('Optimisation Framework Input') 
        self.setWindowIcon(QIcon('NCL.png'))
        self.show()
        
        
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
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
        





