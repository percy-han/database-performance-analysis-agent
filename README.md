# Database Performance Analysis Agent

This project provides a set of tools for diagnosing and analyzing MySQL database performance issues, particularly CPU usage spikes. It uses AI-powered analysis to identify problematic queries and suggest optimizations.

## Overview

The Database Performance Analysis Agent is designed to help database administrators quickly identify the root causes of performance issues in MySQL databases. It analyzes CPU usage patterns, database operations (read, write, update, delete), and slow queries to pinpoint the exact queries causing performance problems.

## Components

### Main Agent

- `agents.py`: The main agent that orchestrates the analysis process using Claude 3.7 Sonnet model. It follows a systematic approach to diagnose CPU usage spikes by analyzing query patterns, correlating them with CPU spikes, investigating slow queries, and determining root causes.

### Analysis Tools

- `plot_diagram_tool.py`: Generates visualizations of CPU usage and database operations (read, write, update, delete) over time to help identify patterns and correlations.
- `snapshot_queries_tool.py`: Analyzes SQL query snapshots, groups similar queries, and generates statistics about their execution times and frequency.
- `database_schema_tool.py`: Retrieves database schema information to help understand table structures and relationships.

### Database Schemas

- `bbb_backend.sql`: Schema for the bbb_backend database.
- `aaa_next_backend_new.sql`: Schema for the aaa_next_backend_new database.

### Analysis Results

- `sql_analysis.json`: Contains the results of SQL query analysis, including execution counts, times, and query patterns.

## How It Works

1. **Data Collection**: The agent collects data on CPU usage and database operations (read, write, update, delete) over time.
2. **Pattern Analysis**: It analyzes patterns in the data to identify correlations between CPU spikes and specific database operations.
3. **Query Investigation**: If a correlation is found, the agent investigates slow queries related to the identified operation type.
4. **Root Cause Determination**: The agent identifies the exact query responsible for the CPU spike and analyzes it against the database schema.
5. **Optimization Suggestions**: Finally, it provides recommendations for optimizing the problematic query.

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd agents

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

To use the Database Performance Analysis Agent:

```python
from agents import agent

# Example: Investigate a CPU spike on a specific server
response = agent("My database server: cn-mysql-db-002, ip: 10.25.63.10. There is a CPU usage spike on 2025-06-01 12:23:12, for 10 mins, please help investigate")
```

The agent will:
1. Generate visualization plots of CPU and database metrics
2. Analyze SQL query snapshots to identify slow queries
3. Correlate query patterns with CPU spikes
4. Provide optimization recommendations

## Requirements

The project requires the following dependencies:

- Python 3.13
- strands (for agent functionality)
- pandas (for data analysis)
- matplotlib (for visualization)
- boto3 (for AWS Bedrock integration)

See `requirements.txt` for a complete list of dependencies.

## Project Structure

```
agents/
├── agents.py                    # Main agent orchestration
├── plot_diagram_tool.py         # Visualization tool
├── snapshot_queries_tool.py     # SQL query analysis tool
├── database_schema_tool.py      # Schema retrieval tool
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── aaa_next_backend_new.sql    # Sample database schema
├── bbb_backend.sql             # Sample database schema
├── sql snapshots.txt           # Sample SQL snapshot data
├── sql snapshots_backup.txt    # Backup SQL snapshot data
└── case-CPU-high-3/            # Sample case data
    ├── CPU - used-data-*.csv
    ├── read rows-data-*.csv
    ├── inserted rows-data-*.csv
    ├── updated rows-data-*.csv
    ├── deleted rows-data-*.csv
    └── 慢 SQL 统计.csv

## License

MIT License - Feel free to use and modify for your needs.
