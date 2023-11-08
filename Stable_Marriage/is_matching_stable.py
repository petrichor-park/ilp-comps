import itertools


def is_matching_stable(
    matching: list[(str, str)],
    pref1: dict[str, list[str]],
    pref2: dict[str, list[str]],
) -> bool:
    # A pair (a, z) is blocking if:
    # - a is paired with some y
    # - z is paired with some b
    # - a prefers z
    # - z prefers a
    matching_12 = {a: b for (a, b) in matching}
    matching_21 = {b: a for (a, b) in matching}

    # Pick each possible pair
    for a, z in itertools.product(pref1.items(), pref2.items()):
        a_name, a_prefs = a
        z_name, z_prefs = z
        # Find out who is already paired: a<->y, b<->z
        y = matching_12[a_name]
        b = matching_21[z_name]
        # Prevent checking if an existing pair is a matching pair
        if a_name == b or z_name == y:
            continue

        a_rank_y = -1
        a_rank_z = -1
        for (idx, name) in enumerate(a_prefs):
            if name == y:
                a_rank_y = idx
            elif name == z_name:
                a_rank_z = idx
        assert a_rank_y != -1 and a_rank_z != -1

        for (idx, name) in enumerate(z_prefs):
            if name == b:
                z_rank_b = idx
            elif name == a_name:
                z_rank_a = idx
        assert z_rank_b != -1 and z_rank_a != -1

        # Preferences are sorted best -> worst, so a lower index
        # is more preferable
        if a_rank_z < a_rank_y and z_rank_a < z_rank_b:
            return False

    return True


if __name__ == "__main__":
    # These examples taken from Gusfield book
    pref1 = {
        "1": ["2", "4", "1", "3"],
        "2": ["3", "1", "4", "2"],
        "3": ["2", "3", "1", "4"],
        "4": ["4", "1", "3", "2"],
    }
    pref2 = {
        "1": ["2", "1", "4", "3"],
        "2": ["4", "3", "1", "2"],
        "3": ["1", "4", "3", "2"],
        "4": ["2", "1", "4", "3"],
    }

    # Men-asking match
    assert is_matching_stable(
        [("1", "4"), ("2", "3"), ("3", "2"), ("4", "1")],
        pref1, pref2
    )

    # Women-asking match
    assert is_matching_stable(
        [("1", "4"), ("2", "1"), ("3", "2"), ("4", "3")],
        pref1, pref2
    )

    # Example bad match
    assert not is_matching_stable(
        [("1", "1"), ("2", "3"), ("3", "2"), ("4", "4")],
        pref1, pref2
    )
