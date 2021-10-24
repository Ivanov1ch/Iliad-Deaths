import os
import statistics
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
deaths_df = pd.read_csv(os.path.join(current_dir, 'data', 'Iliad Death Data.csv'))
lines_df = pd.read_csv(os.path.join(current_dir, 'data', 'Iliad Line Data.csv'))

# Convert 'Y' and 'N' data to boolean
y_n_map_dict = {'Y': True, 'N': False}
deaths_df['Assailant Major Character?'] = deaths_df['Assailant Major Character?'].map(y_n_map_dict)
deaths_df['Victim Major Character?'] = deaths_df['Victim Major Character?'].map(y_n_map_dict)
deaths_df['Victim Killed?'] = deaths_df['Victim Killed?'].map(y_n_map_dict)

# Extract books and data per book
books_in_data = list(deaths_df['Book'].unique())
books_in_data.sort()
book_dfs = [None] * (books_in_data[len(books_in_data) - 1] + 1)

num_books_analyzed = books_in_data[len(books_in_data) - 1]
data_array_length = num_books_analyzed + 1

# Extract line count per book from lines_df
lines_per_book = [None] * data_array_length
for book_num in books_in_data:
    lines_per_book[book_num] = lines_df[lines_df['Book'] == book_num].iloc[0]['Lines']

# Format: [[Greek, Trojan, Total], ...] (index = book)
total_injuries_per_book = [None] * data_array_length
total_lethal_injuries_per_book = [None] * data_array_length
total_nonlethal_injuries_per_book = [None] * data_array_length

total_major_character_injuries_per_book = [None] * data_array_length
total_major_character_lethal_injuries_per_book = [None] * data_array_length
total_major_character_nonlethal_injuries_per_book = [None] * data_array_length

total_minor_character_injuries_per_book = [None] * data_array_length
total_minor_character_lethal_injuries_per_book = [None] * data_array_length
total_minor_character_nonlethal_injuries_per_book = [None] * data_array_length

for book_num in books_in_data:
    book_dfs[book_num] = deaths_df[deaths_df['Book'] == book_num]
    this_df = book_dfs[book_num]

    total_injuries = [0, 0, len(this_df.index)]
    total_lethal_injuries = [0] * 3
    total_nonlethal_injuries = [0] * 3

    major_character_injuries = [0, 0, len(this_df.loc[this_df['Victim Major Character?']].index)]
    major_lethal_injuries = [0] * 3
    major_nonlethal_injuries = [0] * 3

    minor_character_injuries = [0, 0, total_injuries[2] - major_character_injuries[2]]
    minor_lethal_injuries = [0] * 3
    minor_nonlethal_injuries = [0] * 3

    for index, row in book_dfs[book_num].iterrows():
        greek_victim = row['Victim Side'] == 'G'
        side_index = 0 if greek_victim else 1
        is_lethal = row['Victim Killed?']
        major_victim = row['Victim Major Character?']

        total_injuries[side_index] += 1
        if is_lethal:
            total_lethal_injuries[side_index] += 1
            total_lethal_injuries[2] += 1

            if major_victim:
                major_character_injuries[side_index] += 1
                major_lethal_injuries[side_index] += 1
                major_lethal_injuries[2] += 1
            else:
                minor_character_injuries[side_index] += 1
                minor_lethal_injuries[side_index] += 1
                minor_lethal_injuries[2] += 1
        else:
            total_nonlethal_injuries[side_index] += 1
            total_nonlethal_injuries[2] += 1

            if major_victim:
                major_character_injuries[side_index] += 1
                major_nonlethal_injuries[side_index] += 1
                major_nonlethal_injuries[2] += 1
            else:
                minor_character_injuries[side_index] += 1
                minor_nonlethal_injuries[side_index] += 1
                minor_nonlethal_injuries[2] += 1

    total_injuries_per_book[book_num] = total_injuries
    total_lethal_injuries_per_book[book_num] = total_lethal_injuries
    total_nonlethal_injuries_per_book[book_num] = total_nonlethal_injuries

    total_major_character_injuries_per_book[book_num] = major_character_injuries
    total_major_character_lethal_injuries_per_book[book_num] = major_lethal_injuries
    total_major_character_nonlethal_injuries_per_book[book_num] = major_nonlethal_injuries

    total_minor_character_injuries_per_book[book_num] = minor_character_injuries
    total_minor_character_lethal_injuries_per_book[book_num] = minor_lethal_injuries
    total_minor_character_nonlethal_injuries_per_book[book_num] = minor_nonlethal_injuries

# Format: [[Greek, Trojan], ...] (index = book)
ratio_of_damage_done_per_book = [None] * data_array_length
ratio_of_deaths_sustained_per_book = [None] * data_array_length

for book_num in books_in_data:
    book_injuries = total_injuries_per_book[book_num]
    # What ratio of the total injuries were given by each side?
    greek_damage_ratio = round(book_injuries[1] / book_injuries[2], 2)
    trojan_damage_ratio = round(book_injuries[0] / book_injuries[2], 2)

    ratio_of_damage_done_per_book[book_num] = [greek_damage_ratio, trojan_damage_ratio]

    # Similar process with deaths
    book_deaths = total_lethal_injuries_per_book[book_num]
    # What ratio of the total deaths were sustained by each side?
    greek_death_ratio = round(book_deaths[0] / book_deaths[2], 2)
    trojan_death_ratio = round(book_deaths[1] / book_deaths[2], 2)

    ratio_of_deaths_sustained_per_book[book_num] = [greek_death_ratio, trojan_death_ratio]

average_lines_between_injuries = [None] * data_array_length
average_lines_per_injury = [None] * data_array_length

for book_num in books_in_data:
    this_df = book_dfs[book_num]
    num_rows = len(this_df.index)

    lines_between_injuries = []

    for row_index in range(num_rows - 1):
        this_injury_line = this_df.iloc[row_index]['Line']
        next_injury_line = this_df.iloc[row_index + 1]['Line']

        lines_between = int(abs(next_injury_line - this_injury_line))
        lines_between_injuries.append(lines_between)

    average_rows_between = statistics.mean(lines_between_injuries)
    average_lines_between_injuries[book_num] = average_rows_between

    average_lines_per_injury[book_num] = round(lines_per_book[book_num] / total_injuries_per_book[book_num][2], 2)

# Set up results df
results_df_cols = ['Book',
                   'Total Greek Injuries', 'Total Trojan Injuries', 'Total Injuries',
                   'Greek Nonlethal Injuries', 'Trojan Nonlethal Injuries', 'Total Nonlethal Injuries',
                   'Greek Lethal Injuries', 'Trojan Lethal Injuries', 'Total Lethal Injuries',
                   'Total Greek Major Character Injuries', 'Total Trojan Major Character Injuries',
                   'Total Major Character Injuries',
                   'Greek Major Character Nonlethal Injuries', 'Trojan Major Character Nonlethal Injuries',
                   'Total Major Character Nonlethal Injuries',
                   'Greek Major Character Lethal Injuries', 'Trojan Major Character Lethal Injuries',
                   'Total Major Character Lethal Injuries',
                   'Ratio of Injuries Dealt by Greeks', 'Ratio of Injuries Dealt by Trojans',
                   'Ratio of Deaths Sustained by Greeks', 'Ratio of Deaths Sustained by Trojans',
                   'Average Lines Between Injuries', 'Average Lines Per Injury']

results_df = pd.DataFrame(columns=results_df_cols)

for book_num in books_in_data:
    book_df_row = [book_num,
                   total_injuries_per_book[book_num][0], total_injuries_per_book[book_num][1],
                   total_injuries_per_book[book_num][2],
                   total_nonlethal_injuries_per_book[book_num][0], total_nonlethal_injuries_per_book[book_num][1],
                   total_nonlethal_injuries_per_book[book_num][2],
                   total_lethal_injuries_per_book[book_num][0], total_lethal_injuries_per_book[book_num][1],
                   total_lethal_injuries_per_book[book_num][2],
                   total_major_character_injuries_per_book[book_num][0],
                   total_major_character_injuries_per_book[book_num][1],
                   total_major_character_injuries_per_book[book_num][2],
                   total_major_character_nonlethal_injuries_per_book[book_num][0],
                   total_major_character_nonlethal_injuries_per_book[book_num][1],
                   total_major_character_nonlethal_injuries_per_book[book_num][2],
                   total_major_character_lethal_injuries_per_book[book_num][0],
                   total_major_character_lethal_injuries_per_book[book_num][1],
                   total_major_character_lethal_injuries_per_book[book_num][2],
                   ratio_of_damage_done_per_book[book_num][0], ratio_of_damage_done_per_book[book_num][1],
                   ratio_of_deaths_sustained_per_book[book_num][0], ratio_of_deaths_sustained_per_book[book_num][1],
                   average_lines_between_injuries[book_num], average_lines_per_injury[book_num]]
    results_df.loc[len(results_df.index)] = book_df_row

results_df[results_df_cols[0:19]] = results_df[results_df_cols[0:19]].astype(int)
results_df[results_df_cols[19:]] = results_df[results_df_cols[19:]].astype(float)

results_df.to_csv(os.path.join(current_dir, 'out', 'Iliad Death Results.csv'), index=False)
