from pathlib import Path
import pandas as pd

def load_authentication_logs(file_path: Path) -> pd.DataFrame:
    # Read the CSV file and store its rows and columns in a DataFrame.
    logs = pd.read_csv(file_path)

    # Convert the timestamp column from text into Pandas datetime values.
    logs["timestamp"] = pd.to_datetime(
        logs["timestamp"],
        errors="raise",
    )
    # Return the completed DataFrame to the main program.
    return logs