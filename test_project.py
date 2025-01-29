import pytest
import os
from project import FakerData, FileHandler
import tempfile
import shutil
import json
import csv
from pathlib import Path

@pytest.fixture
def faker_data():
    return FakerData()

@pytest.fixture
def file_handler():
    return FileHandler()

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    # Cleanup after tests
    shutil.rmtree(temp_path)
    
def test_faker_functionality_types(faker_data):
    """Test that FakerData class has all required faker functions"""
    required_types = {
        "name", "email", "phone_number", "address", "date",
        "company", "job", "text", "url", "user_name"
    }
    
    available_types = {func["type"] for func in faker_data.formatted_functionality}
    assert required_types.issubset(available_types), "Missing required faker types"
    
    
        
def test_generate_fake_data_single_type(faker_data):
    """Test generating fake data with a single type"""
    selected_types = ["name"]
    num_records = 5
    
    data = faker_data.generate_fake_data(selected_types, num_records)
    
    assert len(data) == num_records
    assert all("name" in record for record in data)
    assert all(isinstance(record["name"], str) for record in data)

def test_generate_fake_data_multiple_types(faker_data):
    """Test generating fake data with multiple types"""
    selected_types = ["name", "email", "phone_number"]
    num_records = 10
    
    data = faker_data.generate_fake_data(selected_types, num_records)
    
    assert len(data) == num_records
    for record in data:
        assert all(key in record for key in selected_types)

def test_generate_fake_data_empty_selection(faker_data):
    """Test generating fake data with no selected types"""
    with pytest.raises(Exception):
        faker_data.generate_fake_data([], 5)

def test_generate_fake_data_invalid_type(faker_data):
    """Test generating fake data with invalid type"""
    with pytest.raises(Exception):
        faker_data.generate_fake_data(["invalid_type"], 5)

def test_csv_file_creation(file_handler, temp_dir):
    """Test CSV file creation with fake data"""
    test_data = [
        {"name": "John Doe", "email": "john@example.com"},
        {"name": "Jane Doe", "email": "jane@example.com"}
    ]
    header = ["name", "email"]
    file_name = Path(temp_dir) / "test_output"
    
    file_handler.write_csv(str(file_name), header, test_data)
    
    # Check if file exists with .csv extension
    csv_path = file_name.with_suffix('.csv')
    assert csv_path.exists()
    
    # Verify CSV content
    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        saved_data = list(reader)
        assert len(saved_data) == len(test_data)
        assert all(record["name"] in [td["name"] for td in test_data] for record in saved_data)

def test_json_file_creation(file_handler, temp_dir):
    """Test JSON file creation with fake data"""
    test_data = [
        {"name": "John Doe", "email": "john@example.com"},
        {"name": "Jane Doe", "email": "jane@example.com"}
    ]
    file_name = Path(temp_dir) / "test_output"
    
    file_handler.write_json(str(file_name), test_data)
    
    # Check if file exists with .json extension
    json_path = file_name.with_suffix('.json')
    assert json_path.exists()
    
    # Verify JSON content
    with open(json_path, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)
        assert saved_data == test_data

def test_file_creation_with_special_characters(file_handler, temp_dir):
    """Test file creation with data containing special characters"""
    test_data = [
        {"name": "João Señor", "email": "joão@example.com"},
        {"name": "Amélie Müller", "email": "amélie@example.com"}
    ]
    header = ["name", "email"]
    file_name = Path(temp_dir) / "test_special_chars"
    
    # Test both CSV and JSON
    file_handler.write_csv(str(file_name), header, test_data)
    file_handler.write_json(str(file_name), test_data)
    
    # Verify CSV content
    with open(file_name.with_suffix('.csv'), 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        csv_data = list(reader)
        assert len(csv_data) == len(test_data)
    
    # Verify JSON content
    with open(file_name.with_suffix('.json'), 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        assert json_data == test_data

def test_large_dataset_generation(faker_data, file_handler, temp_dir):
    """Test handling of large datasets"""
    selected_types = ["name", "email", "phone_number"]
    num_records = 1000
    
    data = faker_data.generate_fake_data(selected_types, num_records)
    file_name = Path(temp_dir) / "large_dataset"
    
    # Test both CSV and JSON with large dataset
    file_handler.write_csv(str(file_name), selected_types, data)
    file_handler.write_json(str(file_name), data)
    
    assert len(data) == num_records
    assert file_name.with_suffix('.csv').exists()
    assert file_name.with_suffix('.json').exists()

def test_file_overwrite(file_handler, temp_dir):
    """Test overwriting existing files"""
    test_data_1 = [{"name": "John Doe"}]
    test_data_2 = [{"name": "Jane Doe"}]
    header = ["name"]
    file_name = Path(temp_dir) / "test_output"
    
    # Write initial files
    file_handler.write_csv(str(file_name), header, test_data_1)
    file_handler.write_json(str(file_name), test_data_1)
    
    # Overwrite with new data
    file_handler.write_csv(str(file_name), header, test_data_2)
    file_handler.write_json(str(file_name), test_data_2)
    
    # Verify CSV content
    with open(file_name.with_suffix('.csv'), 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        csv_data = list(reader)
        assert csv_data[0]["name"] == "Jane Doe"
    
    # Verify JSON content
    with open(file_name.with_suffix('.json'), 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        assert json_data[0]["name"] == "Jane Doe"

def test_error_handling_invalid_path(file_handler):
    """Test error handling for invalid file paths"""
    test_data = [{"name": "John Doe"}]
    header = ["name"]
    
    with pytest.raises(Exception):
        file_handler.write_csv("/invalid/path/test", header, test_data)
    
    with pytest.raises(Exception):
        file_handler.write_json("/invalid/path/test", test_data)