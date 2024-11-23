from collections.abc import MutableSequence
from os import PathLike
from pathlib import Path
from typing import TypeAlias

PathInput: TypeAlias = Path | PathLike[str] | str
PathInputs: TypeAlias = PathInput | MutableSequence[PathInput]
Paths: TypeAlias = Path | MutableSequence[Path]

__all__ = [
    'Path',
    'PathInput'
]
