from rich.table import Table


class MakeTable:
    def mktbl(self, cont: list) -> Table:
        """Make a table list from rich library."""
        l_table = Table(show_header=False)
        l_table.add_column(width=12, justify="center")
        l_table.add_column(width=12, justify="center")

        for lang in cont:
            try:
                l_table.add_row(lang[0], lang[1])
            except IndexError:
                l_table.add_row(lang[0], "")
        return l_table


MakeTable = MakeTable()
