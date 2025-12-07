# Admission Recommender System

A Streamlit-based web application that helps students explore academic programs matching their test scores and interests. The system leverages Apache Spark for efficient data processing and provides intelligent recommendations based on admission criteria.

## Features

- **Smart Program Matching**: Get personalized program recommendations based on your test score
- **Flexible Data Loading**: Upload CSV files or specify file paths
- **Advanced Filtering**: Filter by year, major, program type (paid/free), and admission likelihood
- **Visual Analytics**: Interactive charts showing score distributions and admission probabilities
- **Spark Powered**: Efficient processing of large datasets using Apache Spark

## Prerequisites

- Python 3.8+
- Apache Spark
- Required Python packages (see Installation)

## Installation



1. Install required dependencies:
```bash
pip install requirements.txt
```

2. Ensure Apache Spark is properly configured on your system.



## Configuration

Edit `config.py` to customize default settings:

```python
DEFAULT_CSV_PATH = "path/to/your/data.csv"
PAGE_TITLE = "Admission Recommender System"
LAYOUT = "wide"
SIDEBAR_STATE = "expanded"
TOP_N = 50  # Number of top recommendations to show
```

## Dataset Format

The application expects a CSV file with the following characteristics:

- **Encoding**: UTF-8
- **Delimiter**: Semicolon (`;`)
- **Required Columns** (case-insensitive):
  - `year`: Academic year
  - `major`: Program/major name
  - `score`: Minimum or required score
  - `competition_score`: Competitive score threshold
  - Additional columns as needed

### Example CSV Format:
```csv
year;major;university;score;competition_score;is_paid
2024;Computer Science;Tech University;450.5;520.0;false
2024;Business Administration;State College;400.0;480.5;true
```

## Usage

1. Start the application:
```bash
cd Recommender_System 
streamlit run app.py
```

2. **Load Your Dataset**:
   - Upload a CSV file using the file uploader, or
   - Enter the path to your CSV file in the text input

3. **Configure Filters** (sidebar):
   - Select the academic year
   - Choose or type a major/program
   - Enter your test score
   - Toggle paid programs inclusion
   - Filter by admission likelihood

4. **Get Recommendations**:
   - Click "Find Recommendations"
   - Review matching programs in the results table
   - Explore metrics and visualizations

## Features Explained

### Admission Predictions

- **Likely Admitted**: Your score meets or exceeds the competition score
- **Borderline/Competitive**: Your score is above minimum but below competition score

### Filtering Options

- **Year Filter**: Select specific academic year
- **Major Filter**: Use dropdown or free-text search
- **Score Input**: Slider or numeric input for precision
- **Program Type**: Include/exclude paid programs
- **Likelihood Filter**: Show only likely admission programs

### Visualizations

- **Dataset Preview**: Sample rows from loaded data
- **Metrics Dashboard**: Key statistics about recommendations
- **Score Distribution**: Visual comparison of your score vs program requirements



## Common Issues

1. **File Not Found**:
   - Verify the file path is correct
   - Ensure the file exists and is readable

2. **CSV Parse Errors**:
   - Check that delimiter is semicolon (`;`)
   - Verify UTF-8 encoding
   - Ensure all required columns are present

3. **No Recommendations**:
   - Try adjusting filters (broaden search criteria)
   - Check if your score range matches available programs
   - Verify data quality in the source file

4. **Spark Errors**:
   - Ensure Spark is properly installed
   - Check Java installation (required for Spark)
   - Verify SPARK_HOME environment variable

