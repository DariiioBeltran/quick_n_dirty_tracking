import gspread
import yaml
from gspread import Spreadsheet
from google.oauth2.service_account import Credentials
from models import MesoCycleSchema


def get_sheet(sheet_id: str) -> Spreadsheet:
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)
    return client.open_by_key(sheet_id)

def create_sheet(sheet_name: str) -> Spreadsheet:
    scopes = ["https://www.googleapis.com/auth/spreadsheets", 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)
    return client.create(sheet_name)

def load_workout_from_yaml_file(mesocycle_name: str) -> MesoCycleSchema:
    with open(f"mesocycles/{mesocycle_name}.yaml") as meso:
        raw_meso = yaml.safe_load(meso)
        return MesoCycleSchema.parse_obj(raw_meso)

def calculate_col_letter_from_idx(idx: int) -> str:
    # This is only valid for two letters, beyond that this will NOT work
    offset = ord("A") - 1
    quot = offset + (idx // 26)
    rem = offset + (idx % 26)
    return chr(quot)+chr(rem) if idx > 26 else chr(offset + idx)