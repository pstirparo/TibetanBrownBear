"""Tests for the Entity API."""

import json
import pytest

from yeti.webapp import app

app.testing = True
client = app.test_client()

# pylint: disable=fixme
# TODO: Consider using pytest-flask for easier testing flask stuff, e.g.:
# - Access to url_for objects to test routes
# - Access to .json attribute of request

@pytest.mark.usefixtures("clean_db")
def test_index(populate_malware):
    """Test that a GET request fetches all Entities."""
    rv = client.get('/api/entities/')
    response = json.loads(rv.data)
    assert len(response) == len(populate_malware)
    for element in response:
        assert element['id'].startswith('malware--')

@pytest.mark.usefixtures("clean_db")
def test_get(populate_malware):
    """Test fetching single Entity by ID."""
    rv = client.get('/api/entities/{0:s}/'.format(populate_malware[0].id))
    response = json.loads(rv.data)
    assert isinstance(response, dict)
    assert response['id'] == populate_malware[0].id

@pytest.mark.usefixtures("clean_db")
def test_get_notfound():
    """Test error code when Entity does not exist."""
    rv = client.get('/api/entities/1/')
    assert rv.status_code == 404

@pytest.mark.usefixtures("clean_db")
def test_post():
    """Tests the creation of a new Entity via POST."""
    entity_json = {'name': 'Zeus', 'type': 'malware', 'labels': ['banker']}
    rv = client.post('/api/entities/',
                     data=json.dumps(entity_json),
                     content_type='application/json')
    response = json.loads(rv.data)
    assert response['id'].startswith('malware--')

@pytest.mark.usefixtures("clean_db")
def test_wrong_type_raises_error():
    """Tests that an entity with nonexistent type cannot be created."""
    entity_json = {'name': 'asd', 'type': 'entity.notexist'}
    rv = client.post('/api/entities/',
                     data=json.dumps(entity_json),
                     content_type='application/json')
    assert rv.status_code == 400
    response = json.loads(rv.data)
    assert 'ValidationError' in response
    error_message = response['ValidationError']
    assert '"entity.notexist" not in acceptable datatypes' in error_message

@pytest.mark.usefixtures("clean_db")
def test_put(populate_malware):
    """Tests updating a new object via PUT."""
    rv = client.get('/api/entities/{0:s}/'.format(populate_malware[0].id))
    entity_json = json.loads(rv.data)
    rv = client.put('/api/entities/{0:s}/'.format(entity_json['id']),
                    data=json.dumps({'name': 'NewEntity'}),
                    content_type='application/json')
    response = json.loads(rv.data)
    assert response['id'].startswith('malware--')
    assert response['modified'] != entity_json['modified']

@pytest.mark.usefixtures("clean_db")
def test_filter(populate_malware):
    """Tests searching for specific Entitys based on a name regexp."""
    filter_query = {'name': populate_malware[0].name}
    rv = client.post('/api/entities/filter/',
                     data=json.dumps(filter_query),
                     content_type='application/json')
    response = json.loads(rv.data)
    assert len(response) == 1
