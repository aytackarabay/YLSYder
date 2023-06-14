import pandas as pd
import utils


def Emailer(Program_control_path, Mail_icerigi, Email_listesi_path, Email_konulari_path, hitap):
    program_control = pd.read_excel(Program_control_path)

    utils.Emailer_manager(program_control, 
                utils.Letter_preprocessor(Mail_icerigi, hitap), 
                pd.read_excel(Email_listesi_path), 
                pd.read_excel(Email_konulari_path), hitap)