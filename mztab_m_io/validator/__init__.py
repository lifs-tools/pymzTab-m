from mztab_m_io.validator import custom_checker, default_checker


def init_constraint_checkers() -> None:
    """
    Ensure that the default and custom constraint checker modules are loaded
    so their classes register with the DefaultConstraintCheckerManager.
    """
    import importlib

    importlib.import_module(custom_checker.__name__)
    importlib.import_module(default_checker.__name__)


init_constraint_checkers()
