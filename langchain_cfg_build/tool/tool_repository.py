from typing import Dict

from langchain_core.tools import BaseTool

_ALL_TOOL_MAP: Dict[str, BaseTool] = dict()


class ToolRepository:
    def __init__(self):
        pass


instance: ToolRepository = None


def get_tool_repo():
    global instance
    if not instance:
        instance = ToolRepository()
    return instance


if __name__ == '__main__':
    print('Testing')
