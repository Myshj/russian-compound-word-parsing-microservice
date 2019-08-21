from functools import reduce
from operator import and_

import bottle
import itertools
from pymorphy2 import MorphAnalyzer
from pymorphy2.analyzer import Parse
from pymorphy2.tagset import OpencorporaTag

morph = MorphAnalyzer()


def _tag_to_dict(tag: OpencorporaTag) -> dict:
    return {
        'grammemes': tuple(tag.grammemes)
    }


def _parsed_to_dict(parsed: Parse) -> dict:
    return {
        'normal-form': parsed.normal_form,
        'tag': _tag_to_dict(parsed.tag)
    }


@bottle.route('/parse/<compound>')
def index(compound: str) -> dict:
    words = compound.split(' ')

    if len(words) < 2:
        return {
            'status': 'error',
            'reason': 'no compound provided',
            'compound': compound
        }

    parse_results = tuple(
        morph.parse(word) for word in words
    )
    grammemes = tuple(
        tuple(
            result.tag.grammemes for result in result_list
        ) for result_list in parse_results
    )

    combinations = tuple(itertools.product(*grammemes))
    intersections = tuple(reduce(and_, combination) for combination in combinations)

    intersection_lengths = tuple(
        len(i) for i in intersections
    )
    max_intersection_length = max(intersection_lengths)
    count_of_max = intersection_lengths.count(max_intersection_length)

    if count_of_max != 1:
        return {
            'status': 'error',
            'reason': 'cannot find ideally matching tags',
            'compound': compound
        }

    max_index = intersection_lengths.index(max_intersection_length)

    good_combination = combinations[max_index]

    grammeme_indices = tuple(
        grammemes[i].index(good_combination[i]) for i in range(len(good_combination))
    )

    good_results = tuple(
        parse_results[i][grammeme_indices[i]] for i in range(len(grammeme_indices))
    )

    return {
        'status': 'ok',
        'compound': compound,
        'parsed words': tuple(
            {
                'word': words[i],
                'parsed': _parsed_to_dict(good_results[i])
            } for i in range(len(good_results))
        )
    }


bottle.run(host='localhost', port=8080)
