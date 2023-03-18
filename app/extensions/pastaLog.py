import os
import dateutil.parser
from datetime import datetime


class Pasta:
    def __init__(self):
        self.nomePastaMes = datetime.today().strftime("%m-%Y")
        self.nomePatasDia = datetime.today().strftime("%d")
        
        BASEDIR = os.path.dirname(os.path.realpath(__name__))
        if "G:" in BASEDIR:
            BASEDIR = f"{BASEDIR}GefIII"
        
        self.nomePastaMes = f"{BASEDIR}/app/LOG/{self.nomePastaMes}"
        
        self.nomePatasDia = f"{self.nomePastaMes}/{self.nomePatasDia}"
        
        if not os.path.isdir(self.nomePastaMes):
            os.makedirs(self.nomePastaMes)
        
        if not os.path.isdir(self.nomePatasDia):
            os.makedirs(self.nomePatasDia)
        

    def get_path(self):
        return self.nomePatasDia
        