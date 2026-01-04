import os
import requests
from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv
import datetime
import random

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret')

FREE_DICT_URL = 'https://api.dictionaryapi.dev/api/v2/entries/en/'
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')
PEXELS_URL = 'https://api.pexels.com/v1/search'


def fetch_dictionary(word):
    try:
        r = requests.get(FREE_DICT_URL + word, timeout=8)
        r.raise_for_status()
        data = r.json()
        if isinstance(data, dict) and data.get('title') == 'No Definitions Found':
            return None
        entry = data[0]
        # normalize and enrich entry with aggregated metadata
        try:
            entry = parse_entry(entry)
        except Exception:
            pass
        return entry
    except Exception:
        return None


def fetch_images(query, per_page=6):
    headers = {'Authorization': PEXELS_API_KEY} if PEXELS_API_KEY else None
    params = {'query': query, 'per_page': per_page}
    try:
        # allow calling even when no API key (tests may mock requests.get)
        r = requests.get(PEXELS_URL, headers=headers, params=params, timeout=8)
        r.raise_for_status()
        data = r.json()
        photos = [p['src']['medium'] for p in data.get('photos', [])]
        return photos
    except Exception:
        return []


def parse_entry(entry: dict) -> dict:
    """Enhance a raw dictionary API entry with aggregated synonyms/antonyms/examples.

    Modifies and returns the entry dict so templates can easily display consolidated data.
    """
    # Ensure phonetics, meanings exist
    entry.setdefault('phonetics', [])
    entry.setdefault('meanings', [])

    agg_synonyms = []
    agg_antonyms = []
    examples = []

    for meaning in entry.get('meanings', []):
        for d in meaning.get('definitions', []):
            # normalize lists
            if 'synonyms' in d and isinstance(d['synonyms'], list):
                for s in d['synonyms']:
                    if s and s not in agg_synonyms:
                        agg_synonyms.append(s)
            if 'antonyms' in d and isinstance(d['antonyms'], list):
                for a in d['antonyms']:
                    if a and a not in agg_antonyms:
                        agg_antonyms.append(a)
            if 'example' in d and d['example']:
                examples.append(d['example'])

    entry['aggregated'] = {
        'synonyms': agg_synonyms,
        'antonyms': agg_antonyms,
        'examples': examples,
    }
    # pick first available audio URL from phonetics
    first_audio = None
    for p in entry.get('phonetics', []):
        if isinstance(p, dict) and p.get('audio'):
            first_audio = p.get('audio')
            break
    entry['first_audio'] = first_audio
    return entry


@app.route('/', methods=['GET'])
def index():
    history = session.get('history', [])
    favorites = session.get('favorites', [])
    # word of the day: deterministic based on date
    WORDS = [
        'serendipity', 'aberration', 'ephemeral', 'quintessential', 'eloquent',
        'gossamer', 'lugubrious', 'facetious', 'plethora', 'zenith'
    ]
    idx = datetime.date.today().toordinal() % len(WORDS)
    wotd = WORDS[idx]
    return render_template('index.html', history=history, favorites=favorites, wotd=wotd)


@app.route('/word/<word>', methods=['GET'])
def word_view(word):
    entry = fetch_dictionary(word)
    images = fetch_images(word)

    if entry is None:
        flash(f'No results found for "{word}".', 'danger')
        return redirect(url_for('index'))

    favorites = session.get('favorites', [])
    is_favorite = word.lower() in [w.lower() for w in favorites]
    return render_template('result.html', word=word, entry=entry, images=images, is_favorite=is_favorite)


@app.route('/search', methods=['POST'])
def search():
    word = request.form.get('word', '').strip()
    if not word:
        flash('Please enter a word to search.', 'warning')
        return redirect(url_for('index'))

    # store in history (keep last 10) and redirect to canonical word view
    history = session.get('history', [])
    if word.lower() not in [w.lower() for w in history]:
        history.insert(0, word)
        session['history'] = history[:10]

    return redirect(url_for('word_view', word=word))


@app.route('/favorite', methods=['POST'])
def favorite():
    word = request.form.get('word', '').strip()
    if not word:
        flash('Missing word for favorites.', 'warning')
        return redirect(url_for('index'))

    favorites = session.get('favorites', [])
    lowered = [w.lower() for w in favorites]
    if word.lower() in lowered:
        # remove
        favorites = [w for w in favorites if w.lower() != word.lower()]
        session['favorites'] = favorites
        flash(f'Removed "{word}" from favorites.', 'success')
    else:
        favorites.insert(0, word)
        session['favorites'] = favorites[:50]
        flash(f'Added "{word}" to favorites.', 'success')

    return redirect(url_for('word_view', word=word))
    


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
