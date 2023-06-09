import pandas as pd
import utils


def Emailer(Program_control_path, Mail_icerigi_path, Email_listesi_path, hitap):
    program_control = pd.read_excel(Program_control_path)

    utils.Emailer_manager(program_control, 
                utils.Letter_preprocessor(Mail_icerigi_path, hitap), 
                pd.read_excel(Email_listesi_path), hitap)