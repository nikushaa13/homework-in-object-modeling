from src.rpg.commander import Commander


def main() -> None:
    cmd = Commander()

    g = cmd.create_warrior()
    s = cmd.create_wizard()

    grp = cmd.create_group()
    grp.add(g)
    grp.add(s)

    grp.move(3, 6)

    print(g.display())
    print(s.display())


if __name__ == "__main__":
    main()