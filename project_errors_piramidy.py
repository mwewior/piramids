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
    Raised when there is conflict while solving.
    """
    pass


class InvalidTableError(ProjectErrors):
    """
    Raised when there is conflict on table.
    Usually when:
        1) some table's values exceed maximum height,
        2) there are same values in row or column.
    """
    pass
