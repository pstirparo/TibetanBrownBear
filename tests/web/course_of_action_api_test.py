"""Tests for the Course of Action API."""

import json
import pytest

from yeti.webapp import app

app.testing = True
client = app.test_client()

# pylint: disable=fixme
# TODO: Consider using pytest-flask for easier testing flask stuff, e.g.:
# - Access to url_for objects to test routes
# - Access to .json attribute of request

@pytest.mark.usefixtures('clean_db')
def test_course_of_action_creation():
    query_json = {
        'name': 'Add TCP port 80 Filter Rule',
        'labels': ['block'],
        'type': 'course-of-action',
    }
    rv = client.post('/api/entities/',
                     data=json.dumps(query_json),
                     content_type='application/json')
    response = json.loads(rv.data)
    assert rv.status_code == 200
    assert response['id'].startswith('intrusion-set--')
    assert response['name'] == 'Add TCP port 80 Filter Rule'
    assert response['labels'] == ['block']
