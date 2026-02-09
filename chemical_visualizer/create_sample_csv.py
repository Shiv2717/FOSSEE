"""
Create a sample CSV file for testing the desktop application.

Run this script to generate test_equipment.csv
"""
import csv
import os

# Sample equipment data
equipment_data = [
    ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'],
    ['Pump A', 'Centrifugal', 100.5, 50.2, 25.1],
    ['Pump B', 'Reciprocating', 85.3, 45.8, 26.5],
    ['Compressor X', 'Rotary', 120.0, 60.5, 30.2],
    ['Valve Y', 'Ball', 45.8, 40.1, 22.0],
    ['Turbine Z', 'Centrifugal', 200.5, 75.3, 35.8],
    ['Motor W', 'Electric', 75.2, 52.1, 28.5],
    ['Blower V', 'Axial', 110.3, 55.8, 24.3],
    ['Filter U', 'Mechanical', 30.1, 38.5, 20.1],
]

def create_sample_csv(filename='test_equipment.csv'):
    """
    Create a sample CSV file with equipment data.
    
    Args:
        filename (str): Name of the CSV file to create
    """
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    
    # Write CSV file
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(equipment_data)
    
    print(f"✓ Created sample CSV file: {filename}")
    print(f"  Location: {filepath}")
    print(f"  Records: {len(equipment_data) - 1} equipment entries")
    print("\nYou can now:")
    print("1. Run the desktop app: python desktop_app.py")
    print("2. Click 'Browse...' and select this CSV file")
    print("3. Click 'Upload & Analyze' to test the API connection")
    
    return filepath


if __name__ == '__main__':
    create_sample_csv()
