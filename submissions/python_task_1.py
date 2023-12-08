import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    df.loc[df['id_1'] == df['id_2'], 'car'] = 0
    # pivoting the dataframe to create matrix
    df = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    # returning the matrix
    return df

'''
#Testing generate_car_matrix function :
df1 = pd.read_csv("datasets/dataset-1.csv")
result1 = generate_car_matrix(df1)
print(result1)
'''


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    df['car_type'] = pd.cut (df['car'],bins=[float('-inf'),15, 25,float('inf')], labels=['low', 'medium', 'high'], right=False)
    # count of occurrences for each car_type category
    type_counts = df['car_type'].value_counts().to_dict()
    # sorting alphabetically based on keys
    dictionary = dict(sorted(type_counts.items()))
    # returning dictionary in sorted form
    return dictionary

'''
#Testing get_type_count function:
df2 = pd.read_csv('datasets/dataset-1.csv')
result2 = get_type_count(df2)
print(result2)
'''


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    # finding the mean of the bus column
    meann = df['bus'].mean()
    # finding the index values where bus values are greater than twice the mean
    bus_index = df[df['bus'] > 2 * meann].index.to_list()
    # sorting the index values found
    bus_index.sort()
    # returning list of indexes in sorted form
    return bus_index

'''
#Testing get_bus_indexes function:
df3 = pd.read_csv('datasets/dataset-1.csv')
result3= get_bus_indexes(df3)
print(result3)
'''


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    # average truck values for each route
    route_avg_truck = df.groupby('route')['truck'].mean()
    # filtering routes where the average truck values are greater than 7
    selected_routes = route_avg_truck[route_avg_truck > 7].index.tolist()
    # sort the list of selected routes
    selected_routes.sort()
    # return the sorted list of selected routes
    return selected_routes

'''
#Testing filter_routes function:
df4 = pd.read_csv('datasets/dataset-1.csv')
result4 = filter_routes(df4)
print(result4)
'''


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    # mapping and applying lambda function based on condition
    mod_matrix = matrix.map(lambda x: x * 0.75 if x > 20 else x * 1.25)
    # rounding off the values to 1 decimal place (as shown in sample result dataframe on github)
    mod_matrix = mod_matrix.round(1)
    return mod_matrix

'''
#Testing multiply_matrix function:
inp = result1
result5 = multiply_matrix(inp)
print(result5)
'''

def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    # combining startDay , startTime columns into one column
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

    # combining endDay , endTime columns into one column
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

    # grouping by (`id`, `id_2`) and check completeness
    completeness_check = (
        df.groupby(['id', 'id_2'])
        .apply(lambda group: (
            (group['start_timestamp'].min() == pd.Timestamp('00:00:00')) and
            (group['end_timestamp'].max() == pd.Timestamp('23:59:59')) and
            (len(group['start_timestamp'].dt.dayofweek.unique()) == 7)
        ))
    )

    return completeness_check

'''
#Testing time_check function:
df6 = pd.read_csv('datasets/dataset-2.csv')
result6 = time_check(df6)
print(result6)
'''


#Testing generate_car_matrix function :
df1 = pd.read_csv("datasets/dataset-1.csv")
result1 = generate_car_matrix(df1)
print(result1)
#Testing get_type_count function:
df2 = pd.read_csv('datasets/dataset-1.csv')
result2 = get_type_count(df2)
print(result2)
#Testing get_bus_indexes function:
df3 = pd.read_csv('datasets/dataset-1.csv')
result3= get_bus_indexes(df3)
print(result3)
#Testing filter_routes function:
df4 = pd.read_csv('datasets/dataset-1.csv')
result4 = filter_routes(df4)
print(result4)
#Testing multiply_matrix function:
inp = result1
result5 = multiply_matrix(inp)
print(result5)
#Testing time_check function:
df6 = pd.read_csv('datasets/dataset-2.csv')
result6 = time_check(df6)
print(result6)
