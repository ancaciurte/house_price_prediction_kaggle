
def bathrooms_filler(val):
    if not isinstance(val, str):
        return 1.0
    else:
        return float(val.split(' ')[0])

def floor_level_filler(val):
    if not isinstance(val, str):
        return 1.0
    if 'demisol' in val:
        return -1.0
    if 'parter' in val:
        return 0.0
    elif 'mansarda' in val:
        return 1.0
    elif '0' in val:
        return 0.0
    else:
        return round(eval(val), 3)

def rooms_filler(val):
    if not isinstance(val, str):
        return 1.0
    else:
       return float(val.split(' ')[0])

def state_filler(val):
    if not isinstance(val, str):
        return 'utilizat'
    return val

def surface_filler(val):
    if isinstance(val, str):
        val = eval(val.split(',')[0])
    return float(val)

def zone_aria_filler(val_aria, val_text):
        if not isinstance(val_text, str):
            return val_text if isinstance(val_text, str) else 'Cluj-Napoca'
        if 'Strada' in val_aria:
            return val_aria.replace('Strada ', '')
        else:
            return val_aria
