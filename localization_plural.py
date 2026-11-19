_FALLBACK_LOCALE = "en"


def _plural_category(locale, count):
    if locale == "ru":
        mod10 = count % 10
        mod100 = count % 100
        if mod10 == 1 and mod100 != 11:
            return "one"
        if 2 <= mod10 <= 4 and not 12 <= mod100 <= 14:
            return "few"
        return "many"
    if locale == "en":
        return "one" if count == 1 else "other"
    return "other"


def _render(template, params):
    out = []
    i = 0
    n = len(template)
    while i < n:
        ch = template[i]
        if ch == "{":
            if i + 1 < n and template[i + 1] == "{":
                out.append("{")
                i += 2
                continue
            end = template.find("}", i + 1)
            if end == -1:
                raise ValueError("unbalanced '{' in template")
            name = template[i + 1:end]
            if not name or "{" in name:
                raise ValueError("invalid placeholder in template")
            if name not in params:
                raise ValueError("missing parameter: %r" % name)
            out.append(str(params[name]))
            i = end + 1
        elif ch == "}":
            if i + 1 < n and template[i + 1] == "}":
                out.append("}")
                i += 2
                continue
            raise ValueError("unbalanced '}' in template")
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def format_message(key, locale, params, catalog):
    if not isinstance(catalog, dict):
        raise ValueError("catalog must be a dict")
    if not isinstance(locale, str) or not locale:
        raise ValueError("locale must be a non-empty string")
    if not isinstance(key, str) or not key:
        raise ValueError("key must be a non-empty string")
    if not isinstance(params, dict):
        raise ValueError("params must be a dict")

    messages = catalog.get(locale)
    if messages is None:
        messages = catalog.get(_FALLBACK_LOCALE)
    if messages is None or key not in messages:
        raise ValueError("missing key %r for locale %r" % (key, locale))

    entry = messages[key]
    if isinstance(entry, dict):
        count = params.get("count")
        if isinstance(count, bool) or not isinstance(count, int):
            raise ValueError("count must be a non-negative integer")
        if count < 0:
            raise ValueError("count must be a non-negative integer")
        category = _plural_category(locale, count)
        template = entry.get(category, entry.get("other"))
        if template is None:
            raise ValueError(
                "missing plural form %r for key %r" % (category, key)
            )
    else:
        template = entry
    if not isinstance(template, str):
        raise ValueError("message for key %r must be a string" % key)

    return _render(template, params)
