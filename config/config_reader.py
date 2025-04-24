import json
import os
import datetime


class Bunch:

    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    work_path = None
    subscription_key = None


def read_config():
    """
        Reads config file and unpacks into class object
    """

    # Read config file
    real_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    config_fname = real_path + '/' + 'config.json'
    with open(config_fname) as json_file:
        config = json.load(json_file)

    # Manage directories
    assert os.path.isdir(config['env']['work_dir'])
    assert os.path.isdir(config['env']['data_dir'])

    # Unpack
    config_obj = Bunch(work_dir=config['env']['work_dir'],
                       data_dir=config['env']['data_dir'],
                       settings=config,
                       now_str=datetime.datetime.now().strftime('%Y-%m-%d'),
                       subscription_key=config["subscription_key"],
                       year=config["year"],
                       )

    return config_obj
