import dataclasses
from pathlib import Path

import numpy as np

@dataclasses.dataclass
class MatrixObject(object):
    def to_npz(self, path_npz: Path):
        dict_obj = dataclasses.asdict(self)
        np.savez(path_npz, **dict_obj)

    @classmethod
    def from_npz(cls, path_npz: Path) -> "MatrixObject":
        data = dict(np.load(str(path_npz), allow_pickle=True))
        return MatrixObject(**data)
