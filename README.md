Crime Motives Dashboard
Project Overview
The Crime Motives Dashboard is an interactive data visualization tool built with Streamlit. It provides a comprehensive analysis of crime data, allowing users to explore trends and distributions based on various filtering criteria such as motive, month, and crime type. The dashboard is designed to help analysts and researchers gain insights from processed crime data.
Features
•	Interactive Filters: Use the sidebar to filter data by:
o	Month: Analyze crime data for specific months of the year.
o	General Motive: Categorize crimes into high-level motives (e.g., Sexual Motives, Financial Motives).
o	Specific Motive: Drill down into detailed motive categories (e.g., sexual_violence, dowry).
o	Major Head & Heads of Crime: Filter based on official crime classifications.
•	Dynamic Visualizations: The dashboard features a line chart for monthly trends and a dynamic chart for specific motives that can be toggled between a bar chart and a pie chart.
•	Key Metrics: Get an at-a-glance view of key statistics such as total crimes and the number of unique crime types.
•	Raw Data View: A section is included to view the filtered raw data, which is useful for detailed inspection.
Getting Started
Prerequisites
You will need to have Python installed on your system. It is recommended to use Python 3.7 or higher.
To manage dependencies, you can use pip.
Installation
1.	Clone the repository: If you have this project in a Git repository, clone it to your local machine.
2.	Install the required libraries: Open your terminal or command prompt, navigate to the project directory, and run the following command to install all necessary Python packages:
3.	pip install streamlit pandas plotly

Running the Application
1.	Process the data: Before running the dashboard, you must run the data processing script (data_proccessing.ipynb or a Python equivalent) to generate the enhanced_crime_data.csv file. This file is required for the dashboard to function.
2.	Run the dashboard: From the project directory in your terminal, execute the following command:
3.	python -m streamlit run dashboard_app.py

4.	Your default web browser should open a new tab with the running dashboard. If it doesn't, copy the "Local URL" provided in your terminal and paste it into your browser.
File Structure
The project requires a simple file structure to run correctly:
/your_project_folder
├── dashboard_app.py
├── data_proccessing.ipynb
└── enhanced_crime_data.csv

Usage
•	Use the filter options in the left-hand sidebar to select specific months, motive categories, and crime types.
•	The charts and metrics on the main dashboard will automatically update with each filter selection.
•	Toggle the radio button to switch the "Distribution by Specific Motive" visualization between a bar chart and a pie chart.
Data Source
The dashboard uses the enhanced_crime_data.csv file, which has been pre-processed to clean and standardize the data from various monthly sources. A new super_motive_category column was added to provide a more generalized classification of crime motives for high-level analysis.

