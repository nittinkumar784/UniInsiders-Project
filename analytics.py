import pandas as pd
import csv
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt


with open('/content/social_media_data.csv', mode='r') as file:
    csvFile = csv.reader(file)
    next(csvFile)

    user_actions = {}
    all_actions_counter = Counter()
    user_total_actions = Counter()
    #1
    for row in csvFile:
        user_id = row[0].strip()
        action = row[1].strip()
        if user_id not in user_actions:
            user_actions[user_id] = 1
        else:
            user_actions[user_id] += 1

        all_actions_counter[action] += 1
        user_total_actions[user_id] +=1
        
#2
max_action, max_count = all_actions_counter.most_common(1)[0]

#3
max_user, max_engagement = user_total_actions.most_common(1)[0]

#4
# Load the CSV data
df = pd.read_csv('/content/social_media_data.csv')

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Sort the DataFrame by user_id and timestamp
df.sort_values(by=['user_id', 'timestamp'], inplace=True)

# Initialize variables
sessions = []

# Iterate through the DataFrame
for index, row in df.iterrows():
    if row['action'] == 'login':
        # Record session start time
        session_start_time = row['timestamp']
    elif row['action'] == 'logout':
        # Record session end time and calculate session duration
        session_end_time = row['timestamp']
        if 'session_start_time' in locals() and 'session_end_time' in locals():
            session_duration_seconds = (session_end_time - session_start_time).total_seconds()
            
            # Format session duration as HH:MM:SS
            hours, remainder = divmod(session_duration_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            session_duration = '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
            
            sessions.append({'user_id': row['user_id'], 'session_duration': session_duration})
            del session_start_time  # Reset session_start_time for the next login event

# Create a DataFrame from the result
result_df = pd.DataFrame(sessions)

# Convert session_duration to timedelta for proper summation
result_df['session_duration'] = pd.to_timedelta(result_df['session_duration'])

# Aggregate total session duration for each user
total_session_duration = result_df.groupby('user_id')['session_duration'].sum()


print("--------------")
print("Total Number of actions per user")
print("--------------")
print("User Id : Actions")
for user_id, count in user_actions.items():
    print(f"{user_id}: {count}")
print("--------------\n")
print("\nTotal Count of all actions performed")
print("--------------")
for action, count in all_actions_counter.items():
    print(f"{action}: {count} times")
print("--------------")
print(f"Most Common Action performed: {max_action} ({max_count} times)")
print("--------------\n\n")
print("--------------")
print(f"User with the highest engagement: {max_user} (Total actions: {max_engagement})")
print("--------------\n\n")

print("--------------")
print("Total session Duration for each user on daily basis:")
for user_id, duration in total_session_duration.items():
    print(f"User {user_id}: Total Session Duration {duration}")
print("--------------\n")
plt.bar(total_session_duration.index, total_session_duration.dt.total_seconds() / 3600)  # Convert to hours
plt.xlabel('User ID')
plt.ylabel('Total Session Duration (hours)')
plt.title('Total Session Duration for Each User')
plt.show()