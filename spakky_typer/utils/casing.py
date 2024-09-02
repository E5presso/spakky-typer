import re

PATTERN: re.Pattern[str] = re.compile(r"(?<!^)(?=[A-Z])")


def pascal_to_kebab(pascal_case: str) -> str:
    return PATTERN.sub("-", pascal_case).lower()
