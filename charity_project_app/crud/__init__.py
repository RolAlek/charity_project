__all__ = ["project_crud", "donate_crud"]

from .donate import crud_manager as donate_crud
from .projects import crud_manager as project_crud
