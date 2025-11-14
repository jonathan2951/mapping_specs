# Mapping Specs

A Python tool for generating SQL SELECT queries from structured mapping specifications defined in JSON format.

## Overview

This project provides a framework for defining data transformation mappings using a declarative JSON specification. The mapping specs describe how to transform data from source tables into target tables, including column mappings, joins, filters, and constraints.

## Features

- **Declarative Mapping Specifications**: Define data transformations using JSON
- **SQL Generation**: Automatically generate SQL SELECT queries from mapping specs
- **Structured Format**: Supports sources, joins, filters, columns, constraints, and metadata
- **Type Safety**: Column data types and expectations are defined in the spec

## Project Structure

```
mapping_specs/
├── data/
│   └── mapping_specs.json    # Example mapping specification
├── scripts/
│   └── generate_sql.py       # SQL generation script
├── main.py                    # Main entry point
├── pyproject.toml            # Project configuration
└── README.md                 # This file
```

## Mapping Specification Format

A mapping specification is a JSON object with the following structure:

### Top-Level Fields

- **`_id`**: Unique identifier for the mapping spec (e.g., `"ontology_sport_bags_v1.bag_sku"`)
- **`target`**: Target table configuration
  - `release`: Release name
  - `table`: Target table name
  - `grain`: List of columns that define the grain
  - `partition_by`: List of columns for partitioning
  - `write_mode`: Write mode (e.g., `"merge"`)
- **`sources`**: Array of source table definitions
  - `alias`: Table alias used in SQL
  - `catalog`: Database catalog name
  - `schema`: Database schema name
  - `table`: Table name
- **`joins`**: Array of join definitions
  - `type`: Join type (e.g., `"left"`, `"inner"`)
  - `on`: Array of join conditions (SQL expressions)
- **`filters`**: Array of WHERE clause conditions (SQL expressions)
- **`columns`**: Array of column mappings
  - `target_column`: Name of the target column
  - `expression_sql`: SQL expression for the column
  - `dtype`: Data type (e.g., `"INT"`, `"STRING"`, `"DECIMAL(18,2)"`)
  - `lineage`: Array of source column references
  - `expectations`: Optional validation expectations (e.g., `{"not_null": true}`)
- **`constraints`**: Table constraints
  - `unique_keys`: Array of unique key definitions
  - `fk_checks`: Array of foreign key checks
- **`meta`**: Metadata about the mapping spec
  - `status`: Status of the spec (e.g., `"proposed"`)
  - `generator`: Tool that generated the spec
  - `scores`: Quality scores
  - `created_at`: Creation timestamp
  - `version`: Version information

## Usage

### Generate SQL from a Mapping Spec

```bash
python scripts/generate_sql.py
```

This will read `data/mapping_specs.json` and generate a SQL SELECT query.

### Example Output

Given the example mapping spec, the generated SQL will look like:

```sql
SELECT
    ic.ItemClassID AS BagFamilyId,
    ic.Descr AS BagFamilyName,
    ii.InventoryID AS SKUId,
    ii.InventoryCD AS SKUCode,
    ii.Descr AS Description,
    ii.BasePrice AS ListPrice
FROM group_iii.silver.initemclass AS ic
LEFT JOIN group_iii.silver.inventoryitem AS ii ON ii.ItemClassID = ic.ItemClassID
WHERE ii.InventoryID IS NOT NULL;
```

## Requirements

- Python >= 3.12
- No external dependencies (uses only standard library)

## Development

The project uses `ruff` for linting and code formatting.

### Installation

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

## Example Mapping Spec

See `data/mapping_specs.json` for a complete example of a mapping specification that defines:
- Two source tables (`initemclass` and `inventoryitem`)
- A LEFT JOIN between them
- Column mappings with data types and lineage
- Filters and constraints
- Metadata about the mapping

## License

[Add your license information here]

