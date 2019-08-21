# Compound word analyzer for Russian language
Accepts string consisting of several words split by space.

Uses [pymorphy2](https://github.com/kmike/pymorphy2).

Tries to find out if it is possible to match that words together syntactically.

# Sample
Request: `http://localhost:8080/parse/большой песец`

Response:
```json
{
  "status": "ok",
  "compound": "большой песец",
  "parsed words": [
    {
      "word": "большой",
      "parsed": {
        "normal-form": "большой",
        "tag": {
          "grammemes": [
            "sing",
            "nomn",
            "Qual",
            "ADJF",
            "masc"
          ]
        }
      }
    },
    {
      "word": "песец",
      "parsed": {
        "normal-form": "песец",
        "tag": {
          "grammemes": [
            "sing",
            "nomn",
            "NOUN",
            "anim",
            "masc"
          ]
        }
      }
    }
  ]
}
```

# Caution

May currently stuck in some ambiguous cases, like `большая серая мышь`.

This is because `большая` may actually mean `big` or `bigger than`.
