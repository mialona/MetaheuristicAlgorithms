import pandas as pd

def load_data(path):
    """
    The 'load_data' function manages the collection of operations data from an
    Excel file.

    Args:
        path: Path to Excel file.

    Returns:
        data: List with the values of the operations (columns "ops", "t", "x",
            "y", "seq").
    """

    # Reading the Excel file
    df_data = pd.read_excel(path)

    # Adaptation of the data to its corresponding type (integer or float)
    df_data_int = df_data.astype("int32", copy=True)
    data = df_data_int.values.tolist()
    for i in range(len(data)):
        data[i][1] = float(df_data.at[i,"t"])
        data[i][2] = float(df_data.at[i,"x"])
        data[i][3] = float(df_data.at[i,"y"])

    # Return results
    return data