import pandas as pd
import time

master_log_df = pd.read_csv('master_log.csv')

account_follows = (master_log_df[master_log_df['action'] == 'Follow'].account.value_counts()
 .reset_index()
 .rename(columns = {'index': 'account', 'account': 'follow_count'}))

do_not_unfollow_new = account_follows[account_follows['follow_count'] > 3].account.values

with open('do_not_unfollow.txt') as f:
	do_not_unfollow = f.read().split('\n')

do_not_unfollow = do_not_unfollow + list(do_not_unfollow_new)

time_now = time.strftime('%Y%m%d%H%M')

with open(f'do_not_unfollow_{time_now}.txt', 'w+') as f:
	f.write('\n'.join(do_not_unfollow_new))

with open('do_not_unfollow.txt', 'w+') as f:
	f.write('\n'.join(set(do_not_unfollow)))