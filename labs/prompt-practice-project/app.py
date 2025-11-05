from flask import Flask, request, jsonify
from sqlalchemy import create_engine
import pandas as pd
from typing import List, Dict, Any

app = Flask(__name__)

# Database connection - needs error handling
engine = create_engine('sqlite:///example.db')

def process_data(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    A complex function that processes data and needs refactoring.
    This function does too many things:
    - Validates data
    - Transforms data
    - Calculates statistics
    - Generates reports
    - Saves to database
    """
    result = {}
    
    # Data validation (should be separate)
    for item in data:
        if not all(k in item for k in ['id', 'value', 'category']):
            raise ValueError("Missing required fields")
    
    # Data transformation (should be separate.)
    df = pd.DataFrame(data) 
    df['value'] = df['value'].astype(float)
    df['processed'] = df['value'] * 2
    df['category'] = df['category'].str.upper()
    
    # Statistics calculation (should be separate)
    result['total'] = df['value'].sum()
    result['average'] = df['value'].mean()
    result['max'] = df['value'].max()
    result['min'] = df['value'].min()
    
    # Report generation (should be separate)
    report = {}
    for category in df['category'].unique():
        cat_data = df[df['category'] == category]
        report[category] = {
            'count': len(cat_data),
            'total': cat_data['value'].sum(),
            'average': cat_data['value'].mean()
        }
    result['report'] = report
    
    # Database operations (should be separate)
    df.to_sql('processed_data', engine, if_exists='append', index=False)
    
    return result

# REST API endpoint - needs input validation
@app.route('/api/data', methods=['POST'])
def submit_data():
    data = request.json
    result = process_data(data)
    return jsonify(result)

def basic_sort(arr):
    """
    A basic sorting function that needs improvement.
    Could be improved with:
    - Type hints
    - Better algorithm (currently bubble sort)
    - Input validation
    - Documentation
    - Edge case handling
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def process_user_data(user_info):
    """
    A function that will raise TypeError when given invalid input.
    The error occurs when trying to unpack None.
    """
    name, age = user_info  # Will raise TypeError if user_info is None
    return f"User {name} is {age} years old"

if __name__ == '__main__':
    app.run(debug=True) 