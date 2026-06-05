from nitrogen.backends.base import Backend
import gspread

class GoogleSheetsBackend(Backend):
    def __init__(self, **kwargs):
        creds_path: str | None = kwargs.get("credentials")
        spreadsheet_name: str | None = kwargs.get("spreadsheet")

        if creds_path is not None and spreadsheet_name is not None:
            self.__gc = gspread.service_account(creds_path)
            self.__spreadsheet = self.__gc.open(spreadsheet_name)
    
    def create_sheet(self, sheet):
        self.__spreadsheet.add_worksheet(
            title=sheet.__name__,
            rows=1000,
            cols=23,
        )