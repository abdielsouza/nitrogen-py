import nitrogen.core as nt
from nitrogen.backends import GoogleSheetsBackend

class Students(nt.Sheet, alt_name="Registro de Alunos"):
    id = nt.Column(str, name="ID")
    name = nt.Column(str, name="Nome")
    birthday = nt.Column(str, name="Aniversário")

Students.insert(id="014999", name="Carlos Eduardo", birthday="12/12")

backend = GoogleSheetsBackend(
    credentials="examples/credentials.json",
    spreadsheet="Controle de Classe - Nível 4"
)

nwb = nt.Workbook()
nwb.add(Students)
nwb.sync(backend)

print(Students.schema())