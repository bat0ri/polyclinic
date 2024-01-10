from app.repository.dal import BaseRepo
from app.models.diagnose import Diagnosis



class DiagnoseRepo(BaseRepo[Diagnosis]):
    model = Diagnosis

