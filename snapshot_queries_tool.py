#!/usr/bin/env python3
"""
Script to analyze SQL queries from the SQL snapshots file.
Groups similar queries and generates statistics.
"""

import re
import json
import os
import sys
from collections import defaultdict
from strands import tool

def normalize_sql_query(query):
    """
    Normalize SQL query by replacing specific values with placeholders.
    
    Args:
        query (str): SQL query to normalize
    
    Returns:
        str: Normalized SQL query
    """
    # Replace numeric literals
    normalized = re.sub(r'\b\d+\b', '?', query)
    
    # Replace string literals
    normalized = re.sub(r"'[^']*'", "'?'", normalized)
    normalized = re.sub(r'"[^"]*"', '"?"', normalized)
    
    return normalized

def parse_sql_snapshots(file_path):
    """
    Parse the SQL snapshots file and extract query information.
    
    Args:
        file_path (str): Path to the SQL snapshots file
    
    Returns:
        dict: Dictionary with query information grouped by normalized query
    """
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return None
    
    # Dictionary to store query information grouped by normalized query
    query_groups = defaultdict(lambda: {
        "raw_queries": [],  # Set of unique raw queries
        "count": 0,
        "execution_times": 0,
        "max_execution_time": 0,
        "average_execution_time": 0,
        "db": None  # Database information
    })
    
    # Dictionary to map checksums to statistics
    checksum_stats = {}
    
    # Statistics pattern at the beginning of the file
    stats_pattern = re.compile(r'\[(\-?\d+) => size:(\d+);avgTime:([\d\.]+);maxTime:(\d+),minTime:(\d+)\]')
    
    # Patterns for query information
    time_pattern = re.compile(r'\[Time:(\d+)\]')
    info_pattern = re.compile(r'\[Info:(.*?)\]', re.DOTALL)
    checksum_pattern = re.compile(r'\[checkSum:(\-?\d+)\]')
    db_pattern = re.compile(r'\[db:(.*?)\]')
    
    # Variables to track current query being processed
    current_time = 0
    current_query = ""
    current_checksum = None
    current_db = None
    
    print("Reading statistics from file header...")
    # First pass: collect statistics from the beginning of the file
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        stats_collected = False
        
        for line in f:
            # Check if we've reached the end of the statistics section
            if not stats_collected and line.strip() == "":
                continue
                
            if not stats_collected and "STAT分组:" in line:
                stats_collected = True
                continue
                
            # Try to match statistics pattern
            if not stats_collected:
                stats_match = stats_pattern.search(line)
                if stats_match:
                    checksum = stats_match.group(1)
                    size = int(stats_match.group(2))
                    avg_time = float(stats_match.group(3))
                    max_time = int(stats_match.group(4))
                    
                    # Store statistics by checksum
                    checksum_stats[checksum] = {
                        "count": size,
                        "average_execution_time": avg_time,
                        "max_execution_time": max_time
                    }
    
    print(f"Found statistics for {len(checksum_stats)} query patterns.")
    print("Parsing SQL queries...")
    
    # Let's try a different approach - read the entire file and use regex to extract queries
    print("Reading the entire file...")
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Find all query blocks using regex
    print("Extracting query blocks...")
    query_blocks = re.findall(r'\[db:(.*?)\].*?\[Time:(\d+)\].*?\[Info:(.*?)\].*?\[checkSum:(\-?\d+)\]', content, re.DOTALL)
    
    print(f"Found {len(query_blocks)} query blocks.")
    
    # Process each query block
    query_count = 0
    for db, execution_time_str, query_text, checksum in query_blocks:
        query_count += 1
        if query_count % 100 == 0:
            print(f"Processing query {query_count}...")
        
        current_query = query_groups.get(checksum, {}).get("raw_queries", [])
        if len(current_query) >= 2:
            continue
        
        full_query = ' '.join(line.strip() for line in query_text.strip().split('\n'))

        # Skip empty queries
        if not full_query:
            continue

        if len(current_query) == 0:
            if execution_time_str == str(checksum_stats[checksum]['max_execution_time']):
                query_groups[checksum]["raw_queries"].append(full_query)
                query_groups[checksum]["execution_times"] = checksum_stats[checksum]['max_execution_time']
                query_groups[checksum]["average_execution_time"] = checksum_stats[checksum]['average_execution_time']
                query_groups[checksum]["max_execution_time"] = checksum_stats[checksum]['max_execution_time']
                query_groups[checksum]["count"] = checksum_stats[checksum]['count']
                query_groups[checksum]["db"] = db
        else:
            query_groups[checksum]["raw_queries"].append(full_query)

        
        
        # # Convert execution time to integer
        # try:
        #     execution_time = int(execution_time_str)
        # except ValueError:
        #     execution_time = 0
        
        # # Normalize the query for grouping
        # normalized_query = normalize_sql_query(full_query)
        
        # # Add the raw query to the set
        # query_groups[normalized_query]["raw_queries"].add(full_query)
        
        # # Update execution times
        # query_groups[normalized_query]["execution_times"].append(execution_time)
        
        # # Store database information
        # if not query_groups[normalized_query]["db"]:
        #     query_groups[normalized_query]["db"] = db
        
        # # Update count and statistics from checksum if available
        # if checksum in checksum_stats:
        #     stats = checksum_stats[checksum]
        #     query_groups[normalized_query]["count"] = stats["count"]
        #     query_groups[normalized_query]["max_execution_time"] = stats["max_execution_time"]
        #     query_groups[normalized_query]["average_execution_time"] = stats["average_execution_time"]
    
    print(f"Processed {query_count} queries total.")
    # print("Calculating statistics...")
    
    # # Calculate statistics for queries that don't have them from the header
    # for normalized_query, data in query_groups.items():
    #     # If we don't have count from checksum stats, use the number of execution times
    #     if data["count"] == 0:
    #         data["count"] = len(data["execution_times"])
        
    #     # If we don't have max execution time from checksum stats, calculate it
    #     if data["max_execution_time"] == 0 and data["execution_times"]:
    #         data["max_execution_time"] = max(data["execution_times"])
        
    #     # If we don't have average execution time from checksum stats, calculate it
    #     if data["average_execution_time"] == 0 and data["execution_times"]:
    #         data["average_execution_time"] = sum(data["execution_times"]) / len(data["execution_times"])
        
    #     # Select a representative query from the raw queries
    #     if data["raw_queries"]:
    #         # Choose the shortest query as the representative
    #         data["example_query"] = min(data["raw_queries"], key=len)
    #         # Convert set to list for JSON serialization
    #         data["raw_queries"] = list(data["raw_queries"])
        
    #     # Remove the execution_times list as it's not needed in the output
    #     if "execution_times" in data:
    #         del data["execution_times"]
    
    return query_groups

@tool
def snapshot_queries_tool(server: str, start_time: str, end_time: str):
    """
    Snapshot queries tool is used to load slow read or select logs from the database server.
    The logs are always too big to load for agents, so snapshot queries tool will categorize the logs by checksum, then export to a JSON file.
    Each log will be in following format:
    {
        "raw_queries": [
            "SELECT ...",
            "SELECT ..."
        ],
        "count": 100,
        "max_execution_time": 76, -- seconds
        "average_execution_time": 36.98, -- seconds
        "db": "database"
    }
    The Snapshot queries tool is useful when you need to locate the exact slow read logs. 
    
    Args:
        server: The IP of the server.
        start_time: the start time of the plot diagram
        end_time: the end time of the plot diagram
    
    Returns:
        A file path of slow logs files in JSON format.

    """
    input_file = "sql snapshots.txt"
    output_file = "sql_analysis.json"
    
    print(f"Analyzing SQL queries from: {input_file}")
    
    # Parse SQL snapshots
    query_groups = parse_sql_snapshots(input_file)
    
    if not query_groups:
        print("No queries found or error parsing file.")
        return

    # Convert to list format for output
    query_list = []
    for checksum, data in query_groups.items():
        if data.get("raw_queries"):  # Only include entries with actual queries
            # Create a simplified output structure
            query_entry = {
                "raw_queries": data["raw_queries"],
                "count": data["count"],
                "max_execution_time": data["max_execution_time"],
                "average_execution_time": round(data["average_execution_time"], 2),
                "db": data["db"] if data["db"] else "unknown"
            }
            
            query_list.append(query_entry)
    
    # Sort by count (descending)
    query_list.sort(key=lambda x: x["count"], reverse=True)
    
    print(f"Writing {len(query_list)} unique query patterns to JSON file...")
    
    # Write to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(query_list, f, indent=2, ensure_ascii=False)
    
    print(f"Analysis complete. Results written to: {output_file}")
    print(f"Found {len(query_list)} unique query patterns.")
    
    # Print some statistics
    # if query_list:
    #     top_queries = min(5, len(query_list))
    #     print(f"\nTop {top_queries} queries by count:")
    #     for i in range(top_queries):
    #         query = query_list[i]
    #         print(f"{i+1}. Count: {query['count']}, Max Time: {query['max_execution_time']}ms, Avg Time: {query['average_execution_time']}ms, DB: {query['db']}")
    #         print(f"   Query: {query['example_query'][:100]}..." if len(query['example_query']) > 100 else f"   Query: {query['example_query']}")
    #         print()
    absolute_path = os.path.abspath(output_file)
    return absolute_path

