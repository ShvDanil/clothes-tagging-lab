from typing import Any

from fastapi import UploadFile
from sqlalchemy.orm import Session


class AnnotationNotImplementedError(NotImplementedError):
    pass


def annotate_images(*, images: list[UploadFile], session: Session) -> dict[str, Any]:
    """Implement validation, multi-view inference, scoring and one transactional result.

    You may change this interface and split the implementation into modules.
    All images belong to one item and colour variant. Combine their evidence into
    one annotation and one database record. The result's structure is your design
    decision; see docs/contract.md.
    """
    raise AnnotationNotImplementedError
