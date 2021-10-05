import pickle
from pathlib import Path
from sumo_output_parsers.csv_based_parser.collision_parser import CollisionFileParser
from sumo_output_parsers.csv_based_parser.summary_parser import SummaryFileParser
from sumo_output_parsers.csv_based_parser.statistic_parser import StatisticFileParser
from tempfile import mkdtemp
from sumo_output_parsers.logger_unit import logger

from collections import namedtuple

TestSetting = namedtuple('TestSetting', ('parser_class', 'input_file', 'is_matrix_method', 'metrics'))


def test_csv_based_parser(resource_path_root: Path):
    test_metrics = [
        TestSetting(StatisticFileParser, 'statistic-output.xml', False, []),
        TestSetting(CollisionFileParser, 'collision-output.xml', True, ['collision_victim', 'collision_colliderSpeed']),
        TestSetting(SummaryFileParser, 'summary-output.xml', False, [])
    ]
    for test_args in test_metrics:
        parser = test_args[0](resource_path_root.joinpath(f'output/{test_args.input_file}'))
        parser.xml2csv()
        if isinstance(parser, StatisticFileParser):
            parser.clean_up_dataframe(parser.xml2csv())

        parser.get_attributes()
        if test_args.is_matrix_method:
            for metric in test_args.metrics:
                logger.info(f'file={test_args.input_file} metric={metric}')
                matrix_obj = parser.xml2matrix(metric, agg_func='first')
                path_temp = Path(mkdtemp())
                path_dest = path_temp.joinpath('fcd-matrix.pickle')
                matrix_obj.to_pickle(path_dest)


if __name__ == '__main__':
    test_csv_based_parser(Path('../resources/').absolute())
