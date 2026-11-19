import pytest

import localization_plural as lp

CATALOG = {
    "en": {
        "apple": {"one": "{count} apple", "other": "{count} apples"},
        "hello": "Hello {name}",
    },
    "ru": {
        "apple": {"one": "{count} яблоко", "few": "{count} яблока", "many": "{count} яблок"},
    },
    "ja": {"hello": "こんにちは {name}"},
}


def test_english_one():
    assert lp.format_message("apple", "en", {"count": 1}, CATALOG) == "1 apple"


def test_english_other():
    assert lp.format_message("apple", "en", {"count": 3}, CATALOG) == "3 apples"


def test_english_zero_is_other():
    assert lp.format_message("apple", "en", {"count": 0}, CATALOG) == "0 apples"


def test_russian_one():
    assert lp.format_message("apple", "ru", {"count": 1}, CATALOG) == "1 яблоко"


def test_russian_few():
    assert lp.format_message("apple", "ru", {"count": 3}, CATALOG) == "3 яблока"


def test_russian_many():
    assert lp.format_message("apple", "ru", {"count": 5}, CATALOG) == "5 яблок"


def test_missing_locale_falls_back():
    assert lp.format_message("hello", "fr", {"name": "A"}, CATALOG) == "Hello A"


def test_missing_key_is_rejected():
    with pytest.raises(ValueError):
        lp.format_message("ghost", "en", {}, CATALOG)


def test_missing_param_is_rejected():
    with pytest.raises(ValueError):
        lp.format_message("hello", "en", {}, CATALOG)


def test_extra_param_is_ignored():
    assert lp.format_message("hello", "en", {"name": "A", "x": 1}, CATALOG) == "Hello A"


def test_negative_count_is_rejected():
    with pytest.raises(ValueError):
        lp.format_message("apple", "en", {"count": -1}, CATALOG)


def test_non_integer_count_is_rejected():
    with pytest.raises(ValueError):
        lp.format_message("apple", "en", {"count": 1.5}, CATALOG)


def test_empty_locale_is_rejected():
    with pytest.raises(ValueError):
        lp.format_message("hello", "", {"name": "A"}, CATALOG)


def test_catalog_must_be_dict():
    with pytest.raises(ValueError):
        lp.format_message("hello", "en", {"name": "A"}, [])


def test_output_is_deterministic():
    assert lp.format_message("hello", "en", {"name": "A"}, CATALOG) == "Hello A"
    assert lp.format_message("hello", "en", {"name": "A"}, CATALOG) == lp.format_message("hello", "en", {"name": "A"}, CATALOG)
