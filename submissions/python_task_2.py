import pandas as pd

import warnings
warnings.filterwarnings("ignore")


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    # extracts unique ids from both id_start and id_end columns, combines them into a set, and sorts the result.
    unique_ids = sorted(set(df['id_start'].unique()) | set(df['id_end'].unique()))
    # initializes the distance matrix with zeros, using the unique ids as both row and column indices
    distance_matrix = pd.DataFrame(0, index=unique_ids, columns=unique_ids)

    # setting distances in the matrix
    for index, row in df.iterrows():
        distance_matrix.at[row['id_start'], row['id_end']] = row['distance']

    # calculating cumulative distances
    for via in unique_ids:
        for start in unique_ids:
            for end in unique_ids:
                if start == end:
                    continue

                if distance_matrix.at[start, via] == 0 or distance_matrix.at[via, end] == 0:
                    continue

                if (distance_matrix.at[start, end] == 0 or
                        distance_matrix.at[start, end] > distance_matrix.at[start, via] + distance_matrix.at[via, end]):
                    distance_matrix.at[start, end] = distance_matrix.at[start, via] + distance_matrix.at[via, end]

    # making the matrix symmetric and setting diagonal values to zero:
    distance_matrix = distance_matrix + distance_matrix.T
    distance_matrix.values[[range(distance_matrix.shape[0])]*2] = 0
    df = distance_matrix

    return df

'''
#Testing calculate_distance_matrix function :
df1 = pd.read_csv("datasets/dataset-3.csv")
result1 = calculate_distance_matrix(df1)
print(result1)
'''


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    unrolled_data = []
    # iterating over the rows and columns of the distance matrix
    for start_id in df.index:
        for end_id in df.columns:
            # skip the combination where start_id is equal to end_id
            if start_id == end_id:
                continue
            # extract the distance value for the combination
            distance_value = df.at[start_id, end_id]
            # append the data to the unrolled_data list
            unrolled_data.append({
                'id_start': start_id,
                'id_end': end_id,
                'distance': distance_value
            })
    # creating a dataframe from the unrolled data
    unrolled_df = pd.DataFrame(unrolled_data)
    df = unrolled_df
    return df

'''
#Testing unroll_distance_matrix function :
inp = result1
result2 = unroll_distance_matrix(inp)
print(result2)
'''

def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
    # filer rows with the given reference_id in id_start column
    reference_rows = df[df['id_start'] == reference_id]
    # calculate the average distance for the reference_id
    average_distance = reference_rows['distance'].mean()
    # calculate the 10% threshold range
    threshold_floor = average_distance - 0.1 * average_distance
    threshold_ceiling = average_distance + 0.1 * average_distance
    # filter rows within the 10% threshold range
    within_threshold = df[(df['distance'] >= threshold_floor) & (df['distance'] <= threshold_ceiling)]

    df = within_threshold
    return df

'''    
#Testing find_ids_within_ten_percentage_threshold function :
inp = result2
result3 = find_ids_within_ten_percentage_threshold(df, reference_id=1001410)
print(result3)
'''

def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    # defining rate coefficients for each vehicle type
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}
    # create new columns for each vehicle type and calculate toll rates
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        column_name = f'{vehicle_type}'
        df[column_name] = df['distance'] * rate_coefficient
    return df

'''
#Testing calculate_toll_rate function :
inp = result2
result4 = calculate_toll_rate(inp)
output = result4.drop(columns='distance',axis=0)
print(output)
'''

from datetime import datetime, timedelta, time

def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    all_combinations = []
    # define time ranges
    time_ranges = {
        'weekday_discounts': [(time(0, 0, 0), time(10, 0, 0), 0.8),
                              (time(10, 0, 0), time(18, 0, 0), 1.2),
                              (time(18, 0, 0), time(23, 59, 59), 0.8)],
        'weekend_discount': 0.7
    }
    # generate all combinations
    for day in range(7):  # 0 is monday, 6 is sunday
        for start_time, end_time, discount in time_ranges['weekday_discounts']:
            all_combinations.append((day, start_time, day, end_time, discount))
        all_combinations.append((day, time(0, 0, 0), day, time(23, 59, 59), time_ranges['weekend_discount']))
    
    # create a template dataframe with all possible values
    template_df = pd.DataFrame(all_combinations, columns=['start_day', 'start_time', 'end_day', 'end_time', 'discount'])
    # merge the template_df with the input DataFrame to get all possible combinations
    merged_df = pd.merge(template_df, df, how='cross', suffixes=('_template', '_input'))
    # apply discounts based on the time ranges
    for vehicle in ['moto', 'car', 'rv', 'bus', 'truck']:
        merged_df[vehicle] = merged_df[vehicle] * merged_df['discount']

    # replace numeric days with corresponding weekdays
    merged_df['start_day'] = merged_df['start_day'].map({0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
                                                         4: 'Friday', 5: 'Saturday', 6: 'Sunday'})
    merged_df['end_day'] = merged_df['end_day'].map({0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
                                                     4: 'Friday', 5: 'Saturday', 6: 'Sunday'})
    # dropping the discount column
    merged_df = merged_df.drop(columns='discount',axis=0)
    # rounding off the the float columns with 2 decimal places
    merged_df[['moto', 'car', 'rv', 'bus', 'truck']] = merged_df[['moto', 'car', 'rv', 'bus', 'truck']].round(2)
    # rearranging the columns
    df = merged_df[['id_start', 'id_end', 'distance', 'start_day', 'start_time', 'end_day', 'end_time', 'moto', 'car', 'rv', 'bus', 'truck']]
    # returning the dataframe
    return df
    
    
#Testing calculate_distance_matrix function :
df1 = pd.read_csv("datasets/dataset-3.csv")
result1 = calculate_distance_matrix(df1)
print(result1)
#Testing unroll_distance_matrix function :
inp = result1
result2 = unroll_distance_matrix(inp)
print(result2)
#Testing find_ids_within_ten_percentage_threshold function :
inp = result2
result3 = find_ids_within_ten_percentage_threshold(inp, reference_id=1001430)
print(result3)
#Testing calculate_toll_rate function :
inp = result2
result4 = calculate_toll_rate(inp)
output = result4.drop(columns='distance',axis=0)
print(output)
#Testing calculate_toll_rate function :
inp = result4
result5 = calculate_time_based_toll_rates(inp)
print(result5)

