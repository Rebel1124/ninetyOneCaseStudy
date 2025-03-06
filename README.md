# Ninety One FI Fund Analysis Application

This repository contains the Ninety One Fixed Income Fund case study web application built using Streamlit. The software developed provides tools for pricing fixed rate bonds, classifying bonds into sectors and time buckets, and analyzing/visualizing bond data through interactive tables and graphs.

## Getting Started

Follow these step-by-step instructions to set up and run the application on your local machine.

### Prerequisites

- [Python](https://www.python.org/downloads/) (3.7 or higher)
- [Git](https://git-scm.com/downloads) (for cloning the repository)

### Installation

1. **Clone the repository**

   Open your terminal or command prompt and run the following command:

   ```
   git clone https://github.com/Rebel1124/ninetyOneCaseStudy.git
   ```

   Replace `username/repository-name` with the actual GitHub username and repository name.

2. **Navigate to the project directory**

   ```
   cd repository-name
   ```

   Replace `repository-name` with the name of the folder created by the clone operation.

3. **Install dependencies**

   ```
   pip install -r requirements.txt
   ```

   This command installs all the required Python libraries specified in the requirements.txt file.

### Running the Application

1. **Start the Streamlit application**

   ```
   streamlit run analysis.py
   ```

2. **Access the application**

   The application will automatically open in your default web browser. If it doesn't, you can access it at:
   
   ```
   http://localhost:8501
   ```
   
3. **Access the deployed application**

   You can also access the deployed version of this application at:
   
   ```
   https://ninetyonecasestudy-desireddy.streamlit.app/
   ```

## Application Structure

- **analysis.py**: The main application file that runs the Streamlit interface
- **bondCalculator.py**: Contains functions for pricing fixed rate bonds
- **bondDescritions.py**: Provides logic to classify bonds into sectors and time buckets
- **tablesGraphs.py**: Contains functions for creating Plotly tables and graphs
- **.streamlit/config.toml**: Configuration file for the Streamlit theme and appearance

## Troubleshooting

- If you encounter any issues with dependencies, ensure that you have the correct version of Python installed and that all requirements are properly installed.
- If the application fails to start, check the terminal/command prompt for error messages.
- Make sure all the Python files (analysis.py, bondCalculator.py, bondDescritions.py, and tablesGraphs.py) are in the correct location within the project directory.

## Additional Information

- The application uses Plotly for interactive visualizations and Streamlit for the web interface.
- Custom styling is applied through the .streamlit/config.toml configuration file.