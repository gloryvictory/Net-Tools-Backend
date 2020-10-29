#import time
from time import strftime   # Load just the strftime Module from Time

file_csv = str(strftime("%Y-%m-%d") + "_do_nslookup_network" + ".csv")
file_log = str(strftime("%Y-%m-%d") + "_do_nslookup_network" + ".log")

file_csv_compnames  = 'pc_plus_mode_SN.csv'

folder_in_win = 'D:\\tmp\\'
folder_in_linux = '/Users/glory/projects'

folder_out_win = 'D:\\tmp\\'
folder_out_linux = '/Users/glory/projects'

errors_print = False
errors_log = False

csv_delimiter = ';'

csv_out_dict = {'USERNAME': '',
                'COMPNAME': '',
                'DC': '',
                'DC_IP': '',
                'FQDN': '',
                'FQDN_IP': '',
                'NAME_BY_IP': '',
                'WARNING': '',
                'LASTUPDATE': ''
                } #csv_out_dict


db_host = 'localhost'
db_port = ''
db_user = ''
db_password = ''
db_name = 'net-tools.db'