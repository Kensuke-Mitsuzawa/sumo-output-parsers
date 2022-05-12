import pytest


def pytest_addoption(parser):
    '''
    コマンドラインのオプションを解析し
    --runslow があれば True, なければ False を
    変数として保持する
    '''
    parser.addoption(
        '--visualization',
        action='store_true',
        default=False,
        help='Run tests for visualizations.'
    )
    parser.addoption(
        '--sumo',
        action='store_true',
        default=False,
        help='Run tests that needs SUMO.'
    )


def pytest_configure(config):
    '''
    $ pytest --markers
    上記コマンドで参照できるマーカーの説明を追加します。
    '''
    config.addinivalue_line('markers', 'visualization: test for visualization')
    config.addinivalue_line('markers', 'sumo: when sumo is available')


def pytest_collection_modifyitems(session, config, items):
    # --runslow オプションが無ければ無視します。
    if config.getoption('--visualization'):
        return
    if config.getoption('--sumo'):
        return

    # 独自のスキップマーカー
    skip_slow = pytest.mark.skip(reason='Add --visualization to run tests.')

    # 全テスト対象のメソッドを走査
    for item in items:
        # 'slow'マーカーがあればスキップマーカーを付与
        if 'visualization' in item.keywords:
            item.add_marker(skip_slow)
        if 'sumo' in item.keywords:
            item.add_marker(skip_slow)