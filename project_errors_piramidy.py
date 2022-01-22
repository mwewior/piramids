class ProjectErrors(Exception):
    """
    Parent class for custom errors.
    """
    pass


class InvalidGuideError(ProjectErrors):
    """
    Raised when format of guidance is invalid.
    """
    pass


class PyraminInterposeError(ProjectErrors):
    """
    Raised when some method wants to interpose value
    on other value that already exist in table
    """
    pass


class InvalidTableError(ProjectErrors):
    """
    Raised when there is conflict on table.
    Usually when:\n
    1) some table's values exceed maximum height,\n
    2) there are same values in row or column.
    """
    pass
