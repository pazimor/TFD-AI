from fillroutes import weapons, statistics, cores, archeron, descendants, modules, reactors, external_components
from sql.CRUD.translation_strings import add_translation, get_item

def full(
    weapon = True,
    statistic = True,
    core = True,
    descendant = True,
    module = True,
    reactor = True,
    external = True,
    archerons = True):

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

    if core is True:
        cores.fetch_cores(stats_dict)
        cores.fetch_slots()

    if archerons is True:
        archeron.fill_archeron()

    if descendant is True:
        descendants.fetch_descendants(stats_dict)

    if module is True:
        modules.fetch_modules()

    if reactor is True:
        reactors.fetch_reactors(stats_dict)

    if external is True:
        external_components.fetch_external_components(stats_dict)

    print("finish")
