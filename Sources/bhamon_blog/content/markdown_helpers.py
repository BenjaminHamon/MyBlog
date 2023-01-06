def extract_yaml_header_from_text(text: str) -> str:
    text_lines = text.splitlines()

    separator_indexes = [ index for index, line in enumerate(text_lines) if line == "---" ]
    if len(separator_indexes) == 0:
        raise ValueError("Text contains no YAML header")
    if len(separator_indexes) != 2:
        raise ValueError("Invalid YAML header: bad separators")

    return "\n".join(text_lines[separator_indexes[0] + 1 : separator_indexes[1]]).strip()
