#!/usr/bin/env python3
import pandas as pd
import matplotlib
# Use a non-interactive backend to avoid GUI thread issues
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os
import glob
import math
import numpy as np
import time
from strands import tool

@tool
def plot_diagram_tool(server: str, case_dir: str = "case-CPU-high-1", start_time: str = "", end_time: str = "") -> str:
    """
    Plot diagram tool is used to generate a plot diagram of all CSV metrics found in the sample case directory.
    The plot diagram is useful when analyzing the cause of CPU usage abnormal spike.
    Each CSV file is plotted in its own subplot vertically stacked with a shared time axis.
    The x-axis (time axis) is automatically adjusted to show only the range where data values exist.
    
    Args:
        server: The IP of the server.
        case_dir: The case directory name (e.g., 'case-CPU-high-1', 'case-CPU-high-3'). Defaults to 'case-CPU-high-1'.
        start_time: Optional start time of the plot diagram. If not provided, will use the earliest timestamp with data.
        end_time: Optional end time of the plot diagram. If not provided, will use the latest timestamp with data.
    
    Returns:
        the plot diagram file path
    """
    # Start timing
    start_time_exec = time.time()
    print(f"Starting plot generation at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Define the directory path
    base_path = '/Users/havpan/AWS/Work/Python_Repo/Dev_Stdio/DBA-testing-main/agents/case-CPU-high-3'
    directory_path = os.path.join(base_path, case_dir)
    
    # Find all CSV files in the directory
    csv_files = glob.glob(os.path.join(directory_path, '*.csv'))
    
    if not csv_files:
        return "No CSV files found in the specified directory."
    
    # Dictionary to store dataframes
    dataframes = {}
    
    # Variables to track global time range
    global_min_time = None
    global_max_time = None
    
    # Process each CSV file
    for file_path in csv_files:
        file_name = os.path.basename(file_path)
        print(f"Processing file: {file_name}")
        
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Get column names
        columns = df.columns.tolist()
        if len(columns) < 2:
            print(f"Skipping {file_name} - not enough columns")
            continue
            
        # Standardize time column
        time_col = columns[0]
        metric_col = columns[1]
        
        # Convert time to datetime
        df[time_col] = pd.to_datetime(df[time_col], format='%Y/%m/%d %H:%M')
        
        # Filter out rows with NaN or zero values in the metric column
        # This ensures we only consider timestamps where we have actual data
        df_with_data = df[df[metric_col].notna() & (df[metric_col] != 0)]
        
        if df_with_data.empty:
            print(f"Warning: No valid data points in {file_name}")
            continue
            
        # Update global time range based on timestamps with actual data
        file_min_time = df_with_data[time_col].min()
        file_max_time = df_with_data[time_col].max()
        
        if global_min_time is None or file_min_time < global_min_time:
            global_min_time = file_min_time
        
        if global_max_time is None or file_max_time > global_max_time:
            global_max_time = file_max_time
        
        # Store the dataframe
        dataframes[file_name] = {
            'df': df,
            'time_col': time_col,
            'metric_col': metric_col
        }
    
    # Count the number of files
    num_files = len(dataframes)
    if num_files == 0:
        return "No valid CSV files to plot."
    
    # Create a figure with vertically stacked subplots
    # Each subplot shares the same x-axis (time)
    fig, axes = plt.subplots(num_files, 1, figsize=(15, 3 * num_files), sharex=True)
    
    # Make axes iterable even if there's only one subplot
    if num_files == 1:
        axes = [axes]
    
    # Colors and markers for plots
    colors = ['blue', 'purple', 'red', 'green', 'orange', 'brown', 'pink', 'gray', 'olive', 'cyan']
    markers = ['o', 's', '^', 'd', 'x', '+', '*', 'v', '>']
    
    # Parse user-provided time range if available
    user_start_time = None
    user_end_time = None
    
    if start_time and end_time:
        try:
            user_start_time = pd.to_datetime(start_time)
            user_end_time = pd.to_datetime(end_time)
            # Override global time range with user-specified range only if explicitly provided
            global_min_time = user_start_time
            global_max_time = user_end_time
            print(f"Using user-specified time range: {start_time} - {end_time}")
        except Exception as e:
            print(f"Could not parse user-provided time range: {start_time} - {end_time}. Error: {e}")
            print("Using automatically determined time range based on data.")
    else:
        print(f"Automatically adjusting time axis to data range: {global_min_time} - {global_max_time}")
    
    # Plot each dataset in its own vertically stacked subplot
    for idx, (file_name, data) in enumerate(dataframes.items()):
        ax = axes[idx]
        
        # Create a short label from the file name
        label = file_name.split('.')[0].strip()
        
        # Get the dataframe
        df = data['df']
        time_col = data['time_col']
        metric_col = data['metric_col']
        
        # Plot the data
        ax.plot(
            df[time_col], 
            df[metric_col], 
            marker=markers[idx % len(markers)], 
            linestyle='-', 
            markersize=3, 
            color=colors[idx % len(colors)], 
            label=f'{label} ({metric_col})'
        )
        
        # Add a horizontal line for average value (only considering non-NaN, non-zero values)
        valid_values = df[df[metric_col].notna() & (df[metric_col] != 0)][metric_col]
        if not valid_values.empty:
            avg_value = valid_values.mean()
            ax.axhline(y=avg_value, color='r', linestyle='--', label=f'Average: {avg_value:.4f}')
        
        # Format the subplot
        ax.set_title(f'{label}', fontsize=12)
        ax.set_ylabel(metric_col, fontsize=10)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend(loc='upper right', fontsize=8)
        
        # Format x-axis to show time properly
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        
        # Dynamically adjust the minute interval based on the time range
        time_range_minutes = (global_max_time - global_min_time).total_seconds() / 60
        if time_range_minutes <= 30:
            interval = 5
        elif time_range_minutes <= 60:
            interval = 10
        elif time_range_minutes <= 180:
            interval = 15
        else:
            interval = 30
            
        ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=interval))
        
        # Set the x-axis limits to the global time range for all subplots
        ax.set_xlim(global_min_time, global_max_time)
        
        # Only show x-axis labels on the bottom subplot
        if idx < num_files - 1:
            plt.setp(ax.get_xticklabels(), visible=False)
    
    # Add a common x-axis label only to the bottom subplot
    axes[-1].set_xlabel('Time', fontsize=12)
    
    # Adjust layout for better spacing between subplots
    plt.tight_layout()
    
    # Add a super title for the entire figure
    time_range_str = f"{global_min_time.strftime('%Y-%m-%d %H:%M')} to {global_max_time.strftime('%Y-%m-%d %H:%M')}"
    plt.suptitle(f'Database Metrics for Server: {server}\n{time_range_str}', fontsize=16, y=1.02)
    
    # Save the plot
    output_file = 'metrics_vertical_subplots.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    
    # Get the absolute file path
    absolute_path = os.path.abspath(output_file)
    
    # End timing
    end_time_exec = time.time()
    elapsed_time = end_time_exec - start_time_exec
    print(f"Plot generation completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total execution time: {elapsed_time:.2f} seconds")
    print(f"Plot created and saved as '{absolute_path}'")
    
    # Return the absolute file path
    return absolute_path
