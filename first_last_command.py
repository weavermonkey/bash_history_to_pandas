from os import path
from datetime import datetime
import pandas as pd

history_dict = {'dt':[],'command':[]}
history_timestamps = []
history_commands = []

def create_dataframe_from_bash_history():
	for curr_line in open( path.expanduser( '~/.bash_history' ),'rb' ):
		if curr_line[0] == '#':
			history_timestamps.append( datetime.fromtimestamp( float( curr_line[1:].strip() ) ) )

		elif curr_line[0] != '#' and curr_line != '':
			history_commands.append(curr_line.strip())
	
	for i in range( len( history_timestamps ) ):
		history_dict['dt'].append(history_timestamps[i])
		history_dict['command'].append(history_commands[i])
	
	pd_df = pd.DataFrame.from_dict( history_dict )
	return pd_df

def print_first_last_command_per_day():
	history_df = create_dataframe_from_bash_history()
	history_df['dt'] = pd.to_datetime( history_df['dt'], format='%Y-%m-%d %H:%M:%S' )
	first_commands = history_df.groupby(history_df['dt'].dt.date).first()
	last_commands = history_df.groupby(history_df['dt'].dt.date).last()
	for i in range ( len(first_commands) ):
		print first_commands.dt.iloc[i],first_commands.command.iloc[i],'\n', last_commands.dt.iloc[i],last_commands.command.iloc[i],'\n______________________________'

print_first_last_command_per_day()
