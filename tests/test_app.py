import os
import json
from unittest.mock import patch
from flask import url_for

import pytest

from app import app


class MockResponse:
    def __init__(self, payload, status=200):
        self._payload = payload
        self.status_code = status

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception('HTTP error')


SAMPLE_DICT = [
    {
        "word": "aberration",
        "phonetics": [{"text": "/əˌbɛrəˈʃən/", "audio": "https://audio.example/aberration.mp3"}],
        "meanings": [
            {
                "partOfSpeech": "noun",
                "definitions": [
                    {
                        "definition": "A departure from what is normal, usual, or expected, typically an unwelcome one.",
                        "example": "They described the outbreak of violence in the area as an aberration.",
                        "synonyms": ["anomaly", "deviation"],
                        "antonyms": ["normality"]
                    }
                ]
            }
        ]
    }
]

SAMPLE_PEXELS = {
    'photos': [
        {'src': {'medium': 'https://images.example/1.jpg'}},
        {'src': {'medium': 'https://images.example/2.jpg'}}
    ]
}


def mock_get(url, *args, **kwargs):
    if 'dictionaryapi.dev' in url:
        return MockResponse(SAMPLE_DICT, 200)
    if 'pexels.com' in url:
        return MockResponse(SAMPLE_PEXELS, 200)
    return MockResponse({}, 404)


@patch('requests.get', side_effect=mock_get)
def test_search_aberration(mock_requests, tmp_path):
    app.config['TESTING'] = True
    client = app.test_client()

    resp = client.post('/search', data={'word': 'aberration'}, follow_redirects=True)
    assert resp.status_code == 200
    data = resp.data.decode('utf-8')

    # word present
    assert 'aberration' in data.lower()
    # audio tag present
    assert '<audio' in data
    assert 'audio.example/aberration.mp3' in data
    # synonyms and antonyms
    assert 'synonyms' in data.lower()
    assert 'anomaly' in data
    assert 'normality' in data
    # images present
    assert 'images.example/1.jpg' in data

    # Save snapshot to a fixed repo path for easy inspection
    base = os.path.dirname(__file__)
    repo_snap_dir = os.path.join(base, 'snapshots')
    os.makedirs(repo_snap_dir, exist_ok=True)
    snap_file = os.path.join(repo_snap_dir, 'aberration.html')
    with open(snap_file, 'w', encoding='utf-8') as f:
        f.write(data)

    assert os.path.exists(snap_file)


if __name__ == '__main__':
    pytest.main([__file__])
