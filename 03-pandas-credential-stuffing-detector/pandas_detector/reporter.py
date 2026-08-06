from pathlib import Path
import pandas as pd

def export_findings(
    findings: pd.DataFrame,
    output_file: Path,
) -> Path:
    # Create the output directory when it does not already exist.
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    # Export the DataFrame without Pandas row numbers.
    findings.to_csv(
        output_file,
        index=False,
    )
    # Return the path so the caller can display where the report was saved.
    return output_file