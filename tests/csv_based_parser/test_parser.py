import pickle
from pathlib import Path
from sumo_output_parsers.csv_based_parser.collision_parser import CollisionFileParser
from tempfile import mkdtemp


def test_csv_based_parser(resource_path_root: Path):
    test_metrics = [
        (CollisionFileParser, 'collision-output.xml', ['collision_victim', 'collision_colliderSpeed'])
    ]
    for test_args in test_metrics:
        parser = test_args[0](resource_path_root.joinpath(f'output/{test_args[1]}'))
        df_csv = parser.xml2csv()
        attributes = parser.get_attributes()
        for metric in test_args[2]:
            matrix_obj = parser.xml2matrix(metric)
            path_temp = Path(mkdtemp())
            path_dest = path_temp.joinpath('fcd-matrix.pickle')

            matrix_obj.to_pickle(path_dest)
            # matrix_obj_file = FcdMatrixObject.from_pickle(path_dest)


if __name__ == '__main__':
    test_csv_based_parser(Path('../resources/'))
