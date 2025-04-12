from fillroutes import weapons
from fillroutes import statistics
from sql.CRUD.translation_strings import add_translation, get_item

def full(weapon = True, statistic = True):

    ## init default
    if get_item(1) == []:
        add_translation(**{
            "fr": None,
            "ko": None,
            "en": None,
            "de": None,
            "ja": None,
            "zh_cn": None,
            "zh_tw": None,
            "it": None,
            "pl": None,
            "pt": None,
            "ru": None,
            "es": None
        })

    stats_dict = {}
    if statistic is True:
        stats_dict = statistics.fetch_statistics()

    ## stats_dict is a dict with stats_id once set inside DB
    ## so ready to send to others

    if weapon is True:
        weapons.fetch_weapons(stats_dict)
    print("finish")
