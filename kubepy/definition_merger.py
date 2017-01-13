import itertools
import functools


@functools.singledispatch
def merge_definitions(*definitions):
    return definitions[-1]


@merge_definitions.register(dict)
def merge_dicts(*definitions):
    keys = set(itertools.chain(*(definition.keys() for definition in definitions)))
    result = {}
    for key in keys:
        result[key] = merge_definitions(*(definition[key] for definition in definitions if key in definition))
    return result


@merge_definitions.register(list)
@merge_definitions.register(tuple)
def merge_lists(*definitions):
    named_results = {}
    unmerged_results = []
    for definition in itertools.chain(*definitions):
        if hasattr(definition, '__getitem__') and 'name' in definition:
            name = definition['name']
            if name in named_results:
                named_results[name].append(definition)
            else:
                new_result = [definition]
                named_results[name] = new_result
                unmerged_results.append(new_result)
        else:
            unmerged_results.append([definition])
    return list(merge_definitions(*results) for results in unmerged_results)
