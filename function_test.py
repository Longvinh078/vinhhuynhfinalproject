import pytest
from main import get_release_date, get_lyrics, get_info

test_release_date = '2015-11-20'
test_lyrics = "Hello, it's me\nI was wondering if after all these years you'd like to meet\nTo go over everything\nThey " \
           "say that time's supposed to heal ya, but I ain't done much healing\n\nHello, can you hear me?\nI'm in " \
           "California dreaming about who we used to be\nWhen we were younger and free\nI've forgotten how it felt " \
           "before the world fell at our feet\n\nThere's such a difference between us\nAnd a million miles\n\nHello " \
           "from the other side\n\nI must've called a thousand times\nTo tell you I'm sorry for everything that I've " \
           "done\nBut when I call, you never seem to be home\n\nHello from the outside\n...\n\n******* This Lyrics is " \
           "NOT for Commercial use *******\n(1409623768306)"

def test_get_release_date():
    # Test with a known album_id
    release_date = get_release_date('20883397')
    assert release_date == test_release_date


def test_get_lyrics():
    # Test with a known song title and artist
    lyrics = get_lyrics('Hello', 'Adele')
    assert test_lyrics in lyrics

