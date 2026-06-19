import nitrogen.core as nt
from nitrogen.backends import GoogleSheetsBackend

class Students(nt.Sheet, name="Registro de Alunos"):
    id = nt.Column(str)
    name = nt.Column(str, name="nome")
    birthday = nt.Column(str, name="aniversário")

Students.insert(id="001144", name="Anna Clara", birthday="00/00/00")

backend = GoogleSheetsBackend(
    credentials="./credentials.json",
    spreadsheet="Controle de Classe - Nível 4"
)

nwb = nt.Workbook()
nwb.add(Students)
nwb.sync(backend)