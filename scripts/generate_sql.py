import json
from textwrap import indent


def generate_select_sql(mapping_spec: dict) -> str:
    # --- Step 1: Build SELECT clause
    select_clauses = [
        f"    {col['expression_sql']} AS {col['target_column']}"
        for col in mapping_spec["columns"]
    ]
    select_sql = ",\n".join(select_clauses)

    # --- Step 2: Sources dictionary for lookup
    sources = {s["alias"]: s for s in mapping_spec["sources"]}

    # --- Step 3: Build FROM + JOIN clauses
    used_aliases = set()
    sql_lines = []

    # Pick the first source as the base
    base_alias = mapping_spec["sources"][0]["alias"]
    base = sources[base_alias]
    sql_lines.append(
        f"FROM {base['catalog']}.{base['schema']}.{base['table']} AS {base_alias}"
    )
    used_aliases.add(base_alias)

    # Process joins iteratively
    for join in mapping_spec.get("joins", []):
        join_type = join["type"].upper()
        join_condition = " AND ".join(join["on"])

        # Extract aliases from the ON condition
        aliases_in_join = {cond.split(".")[0] for cond in join["on"] if "." in cond}

        # Find which alias we haven’t joined yet
        new_aliases = aliases_in_join - used_aliases
        if not new_aliases:
            # Already processed both aliases
            continue

        # Assume only one new alias is introduced per join
        new_alias = new_aliases.pop()
        if new_alias not in sources:
            raise ValueError(f"Alias '{new_alias}' not found in sources")

        s = sources[new_alias]
        sql_lines.append(
            f"{join_type} JOIN {s['catalog']}.{s['schema']}.{s['table']} AS {new_alias} ON {join_condition}"
        )
        used_aliases.add(new_alias)

    # --- Step 4: Filters (WHERE)
    filters = mapping_spec.get("filters", [])
    where_sql = ""
    if filters:
        where_sql = "WHERE " + " AND ".join(filters)

    # --- Step 5: Combine all
    sql = f"""SELECT
{select_sql}
{chr(10).join(sql_lines)}
"""
    if where_sql:
        sql += where_sql + "\n"

    return sql.strip() + ";"


if __name__ == "__main__":
    filepath = "data/mapping_specs.json"
    with open(filepath, "r") as f:
        data = json.load(f)
    sql_query = generate_select_sql(mapping_spec=data)
    print(f"{sql_query=}")
