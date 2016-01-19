import collections


def update_recursive(d, u):
    """
    Update dict in recursive manner.

    :param d: dict to be updated
    :param u: dict containing values d will be updated with
    """
    for k in u.keys():
        if isinstance(u[k], collections.Mapping) and isinstance(d.get(k, None), collections.Mapping):
            update_recursive(d[k], u[k])
        else:
            d[k] = u[k]

