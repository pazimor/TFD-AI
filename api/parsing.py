import re

def parse_effect_line(effect_str, stat_dict):
    """
    :param effect_str:
    :param stat_dict:
    :return: parsed effect line
    """
    # Normalize the effect string, replacing non-breaking spaces with regular spaces
    normalized = effect_str.replace("\u00A0", " ").replace("\n", " ").strip()
    normalized = normalized.rstrip(" .")

    # Build an inverted mapping: stat name -> key from stat_dict
    inverted = {}
    for key, value in stat_dict.items():
        if isinstance(value, dict) and "id" in value:
            # Use the stat name from value["name"] if available, otherwise use value["id"]
            stat_name = value.get("name", value["id"])
            inverted[stat_name] = key
        else:
            inverted[value] = key

    # Split the effect string by comma to handle multiple simple effects
    parts = [part.strip() for part in normalized.split(",")]
    results = {}
    simple_pattern = re.compile(r"^([\wÀ-ÖØ-öø-ÿ\s'-]+)\s*([+-]\d+(?:[.,]\d+)?\s*%?)$", re.IGNORECASE)
    simple_found = False
    for part in parts:
        m = simple_pattern.match(part)
        if m:
            simple_found = True
            stat_name = m.group(1).strip()
            modifier = m.group(2).replace(" ", "")
            if "%" in part and "%" not in modifier:
                modifier += "%"
            key_to_use = inverted.get(stat_name, stat_name)
            results[key_to_use] = modifier

    if simple_found:
        return results
    else:
        # If no simple effect is found, perform a template extraction on the entire normalized string
        num_pattern = re.compile(r"(\d+(?:[.,]\d+)?\s*(?:%|s))")
        values = []
        counter = 1

        def replacement(match):
            nonlocal counter, values
            num_str = match.group(0).strip().replace(" ", "")
            # Normalize decimal separator
            num_str = num_str.replace(",", ".")
            values.append(num_str)
            placeholder = "{" + str(counter) + "}"
            counter += 1
            return placeholder

        template = num_pattern.sub(replacement, normalized)
        return {template: values}

if __name__ == '__main__':
    effect_str = "DÉF +89.8 %."
    stat_dict = {"10": "DÉF"}
    print("Input:", effect_str)
    print("Output:", parse_effect_line(effect_str, stat_dict))
    print("-" * 40)

    effect_str = "DÉF +89.8 %, puissance des compétences +8.1 %."
    stat_dict = {"10": "DÉF", "12": "puissance des compétences"}
    print("Input:", effect_str)
    print("Output:", parse_effect_line(effect_str, stat_dict))
    print("-" * 40)

    effect_str = "Infliger un coup critique avec une compétence confère Tirs concentrés, ce qui augmente les dégâts critiques des armes à feu de 12.4% pendant 15s. Infliger un coup critique avec une arme à feu confère Concentration archéonique, ce qui augmente les dégâts critiques des compétences de 46% pendant 15s . Vous ne pouvez bénéficier que d'un seul effet à la fois"
    stat_dict = {"10": "DÉF", "12": "puissance des compétences"}
    print("Input:", effect_str)
    print("Output:", parse_effect_line(effect_str, stat_dict))
    print("-" * 40)