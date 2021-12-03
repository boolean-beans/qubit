class QubitBaseException(Exception):
    """base class from which all Qubit exceptions inherit from"""
    pass


class HierarchyError(QubitBaseException):
    """exception raised when one user cannot commit
    a moderation action due to the role heirarchy"""
    pass


class SelfModError(QubitBaseException):
    """exception raised when user attempts to
    commit moderation action to themself"""
    pass
