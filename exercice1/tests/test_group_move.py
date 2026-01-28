from src.rpg.commander import Commander


def test_group_move_moves_all_units():
    cmd = Commander()

    g = cmd.create_warrior()
    s = cmd.create_wizard()

    grp = cmd.create_group()
    grp.add(g)
    grp.add(s)

    grp.move(3, 6)

    assert g.position.x == 3
    assert g.position.y == 6
    assert s.position.x == 3
    assert s.position.y == 6