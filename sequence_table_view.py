"""
Build an HTML table view of certain query fields for Sequences.
"""
from typing import List, Any
import utils.shotgrid
import shotgun_api3

def open_sequence_table(project_id: int) -> None:
    """
    Opens up an HTML based sequence table for via a project ID.

    Args:
        project_id (int): The SG id of a project to open the table for.
    """
    ...

def _build_html(table_data: List[dict]) -> str:
    """
    Uses the evaluated table data to build HTML as a string and returns it.

    Args:
        table_data (List[dict]): The table data to render into HTML.

    Returns:
        str - The generated HTML as a string.
    """
    ...

def _evaluate_shotgrid_query_field(sg: shotgun_api3.Shotgun, entity: dict, query_field: str) -> Any:
    """
    Returns back the expected result from an SG Query field for a certain entity.

    Args:
        sg (shotgun_api3.Shotgun): The SG connection object.
        entity (dict): The SG entity dictionary - Requires an 'id' and 'type' field.
        query_field (str): The query field to evaluate.

     Returns:
        Any - The evaluated query field, data structure could change depending on the query field.
    """
    ...

if __name__ == "__main__":
    project_id = 85
    open_sequence_table(project_id)
