def _json_parser(json_data: dict) -> str:
    elements = json_data.get("elements")
    messageml = ""
    for element in elements:
        tag = element["tag"]
        text = element["text"]
        attributes = element["attributes"]
        messageml += f"<{tag}"
        for attr_key, attr_val in attributes.items():
            messageml += f' {attr_key}="{attr_val}"'
        messageml += f">{text}"
        if "elements" in element:
            for inner_element in element["elements"]:
                inner_messageml = _json_parser({"elements": [inner_element]})
                messageml += inner_messageml
        messageml += f"</{tag}>"
    return messageml


def build_messageML(payload: dict) -> str:
    return f"<messageML>{_json_parser(payload)}</messageML>"
