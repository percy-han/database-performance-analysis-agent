import os
from strands import tool

@tool
def database_schema_tool(db: str) -> str:
    """
    Given database name and get the schema for the database. 
    
    Args:
        db (str): The database name.
    
    Returns:
        str: The absolute file path to the database schema.
    """
    # Get the current working directory
    current_directory = os.getcwd()
    
    # Construct the path to the plot image
    schema_path = os.path.join(current_directory, f"{db}.sql")
    
    # Return the path to the plot image
    return schema_path