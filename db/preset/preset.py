"""Module "db"
"""


class Preseter(object):
    """Cool presetter who knows how to do some things
    actions on the default MySQL database by calling
    just one function. Required, for example, for installation
    standard settings, tables, etc.
    """
    def __init__(self, connection, cursor):
        self.con = connection
        self.cur = cursor


    # add custom presets
