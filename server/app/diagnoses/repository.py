from app.dal import BaseRepo
from app.diagnoses.model import Diagnosis



class DiagnoseRepo(BaseRepo[Diagnosis]):
    model = Diagnosis

