import pickle
from pathlib import Path
from sumo_output_parsers import FCDFileParser, FcdMatrixObject
from tempfile import mkdtemp


def test_fcd_output(resource_path_root: Path):
    parser = FCDFileParser(resource_path_root.joinpath('output/fcd-output.xml'))
    matrix_obj = parser.xml2matrix('lane', skip_intervals=100)
    path_temp = Path(mkdtemp())
    path_dest = path_temp.joinpath('fcd-matrix.pickle')

    matrix_obj.to_pickle(path_dest)
    matrix_obj_file = FcdMatrixObject.from_pickle(path_dest)

    p_cache = parser.generate_cache_path(method_name='xml2matrix', suffix=parser.encode_parameters(
        path_file=str(parser.path_file),
        target_element='lane',
        skip_intervals=100))
    assert p_cache.exists()


if __name__ == '__main__':
    test_fcd_output(Path('resources/'))
