import glob
import pandas as pd

def make_master_log():
    logs = glob.glob('log_*.csv')
    log_dfs = []
    for l in logs:
        log_dfs.append(pd.read_csv(l))
        master_log_df = pd.concat(log_dfs, ignore_index = True)
    master_log_df.to_csv('master_log_test.csv', index = False)


make_master_log()