"""
Build an HTML table view of certain query fields for Sequences.
"""
from typing import List, Any
import utils.shotgrid
import shotgun_api3
from pprint import pprint

def open_sequence_table(project_id: int) -> None:
    """
    Opens up an HTML based sequence table for via a project ID.

    Args:
        project_id (int): The SG id of a project to open the table for.
    """
    sg = utils.shotgrid.get_shotgrid_python_client()
    sequences = sg.find("Sequence", filters=[["project.Project.id", "is", project_id]], fields=["code"])
    table_data = _build_table_data(sg, sequences)


def _build_table_data(sg, sequences: List[dict]) -> List[dict]:
    """
    Evalutes and structures the fields needed to render the table.

    Args:
        sg (shotgun_api3.Shotgun): The SG connection object.
        sequences (List[dict]): A list of SG sequence entity dictionaries.

    Returns:
        List[dict]: A list of dictionaries containing the necessary fields used in the table.
    """
    table_data = []
    for sequence in sequences:
        row_data = {}
        row_data["ID"] = sequence.get("id")
        row_data["Code"] = sequence.get("code")
        row_data["Average Cut Duration"] = _evaluate_shotgrid_query_field(sg, sequence, "sg_cut_duration")
        # row_data["IP Versions"] = _evaluate_shotgrid_query_field(sg, sequence, "sg_ip_versions")
        table_data.append(row_data)
    table_data.sort(key=lambda x: x.get("id"))
    pprint(table_data)
    return table_data

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
    #TODO First pass, needs handling for deeper filter structures
    field_schema = sg.schema_field_read(entity.get("type"), field_name=query_field)
    pprint(field_schema)
    field_properties = field_schema[query_field]["properties"]
    query_data = field_properties["query"]["value"]
    entity_type = query_data["entity_type"]
    filter_schemas = query_data["filters"]["conditions"]
    summary_filters = []
    for filter_schema in filter_schemas:
        if filter_schema["active"] == "true":
            # Parse out if a filter is set to "Current X"
            filter_values = filter_schema["values"]
            replaced_filter_value = []
            for filter_value in filter_values:
                if filter_value.get("id") == 0 and filter_value.get("name") == f"Current {entity.get('type')}":
                    replaced_filter_value.append(entity)
                else:
                    replaced_filter_value.append(filter_value)
            if len(filter_values) == 1 and filter_schema["relation"] == "is":
                replaced_filter_value = replaced_filter_value[0]
                    
            
            summary_filters.append([filter_schema["path"], filter_schema["relation"], replaced_filter_value])


    summary_fields = []
    summary_fields.append({"field": field_properties["summary_field"]["value"], "type": field_properties["summary_default"]["value"]})
    summary = sg.summarize(entity_type, filters=summary_filters, summary_fields=summary_fields)
    return summary["summaries"][query_field]

if __name__ == "__main__":
    project_id = 85
    open_sequence_table(project_id)
