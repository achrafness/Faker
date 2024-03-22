import pytest
import os
from project import write_json ,write_csv , generate_fake_data 

def test_valid_write_csv():
    header = ['name', 'age', 'city']
    data = [
        {'name': 'Alice', 'age': 24, 'city': 'Toronto'},
        {'name': 'Bob', 'age': 25, 'city': 'Vancouver'},
        {'name': 'Charlie', 'age': 26, 'city': 'Montreal'}
    ]
    write_csv('test', header, data)
    assert os.path.exists('test.csv')
    os.remove('test.csv')
def test_empty_write_csv():
    header = []
    data = []
    with pytest.raises(ValueError):
        write_csv('test', header, data)
def test_invalid_write_csv():
    header = {'name':"coco", 'age':14, 'city':"khenchela"}
    data = "name,age,city"
    with pytest.raises(ValueError):
        write_csv('test', header, data)

def test_valid_write_json():
    data = {
        'name': 'Alice',
        'age': 24,
        'city': 'Toronto'
    }
    write_json('test', data)
    assert os.path.exists('test.json')
    os.remove('test.json')
def test_empty_write_json():
    data = {}
    with pytest.raises(ValueError):
        write_json('test', data)
def test_invalid_write_json():
    data = "name,age,city"
    with pytest.raises(ValueError):
        write_json('test', data)

def test_generate_fake_data():
    selected_choices = ["name", "email", "phone_number"]
    number_of_items = 10
    fake_data = generate_fake_data(selected_choices, number_of_items)
    assert len(fake_data) == number_of_items
    for data in fake_data:
        assert all(choice in data for choice in selected_choices)
    