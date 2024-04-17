def str_to_bool(string: str) -> bool:
    if not isinstance(string, str):
        raise ValueError(f'string must be an instance of type str, but {type(string)} was provided')
    s = string.lower()
    return s in ['1', 'true', 'y', 't', 'yes']
