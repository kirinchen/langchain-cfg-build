from typing import List, Union, cast

from langchain.agents import BaseSingleActionAgent, BaseMultiActionAgent, create_react_agent, AgentExecutor
from langchain_core.tools import BaseTool

from langchain_cfg_build.app import initialize
from langchain_cfg_build.llm.enum_llm import EnumLLM
from langchain_cfg_build.prompt.enum_prompt import EnumPrompt


class AgentBuilder:
    llm: EnumLLM
    tools_cfg_list: List[dict]
    prompt: EnumPrompt

    def __init__(self,
                 llm: EnumLLM,
                 tools_cfg_list: List[dict],
                 prompt: EnumPrompt
                 ):
        self.llm = llm
        self.prompt = prompt
        self.tools_cfg_list = tools_cfg_list
        self._tools: List[BaseTool] = self._list_tool_instance_by_cfg()

    def __repr__(self):
        tools_repr = ", ".join(tool.name for tool in self.tools)
        return (f"AgentBuilder(llm={self.llm.name}, "
                f"tools=[{tools_repr}], "
                f"prompt={self.prompt.name})")

    def _list_tool_instance_by_cfg(self) -> List[BaseTool]:
        return [tool_service.gen_tool(**tool) for tool in self.tools_cfg_list]

    def create_agent(self) -> Union[BaseSingleActionAgent, BaseMultiActionAgent]:
        # tools = self.list_tool_instance()
        # tools.extend(self.list_tool_instance_by_cfg())
        return cast(BaseSingleActionAgent,
                    create_react_agent(self.llm.value.get_instance(), self._tools, self.prompt.value.get_instance()))

    def build_executor(self) -> AgentExecutor:
        agent = self.create_agent()
        ans = AgentExecutor(agent=agent, tools=self._tools, verbose=True, )
        return ans


if __name__ == '__main__':
    initialize()
    agent_builder = AgentBuilder(
        EnumLLM.gpt_4o,
        [],
        EnumPrompt.HWCHASE17_REACT
    )
    agent_executor = agent_builder.build_executor()
    # query = "Please help me find domiearth company email?"
    # tchu@domiearth.com
    # query = """Please help me write to tchu@domiearth.com.
    # Is there any relevant information about Taipei Weather?
    #  and mark this as a test letter sent by Kirin’s AI assistant"""
    # query = "如果我有一個具有兩邊長度分別為51公分和34公分的三角形，那麼斜邊的長度是多少呢？"
    # query = 'Show Comm.java.java source code for my project?'
    # query = '列出ENC 投影片中有關家庭的頁碼,將此產生一個新的ppt'
    query = '給個json格式的範例'
    # query = 'What is the main focus of this project?'
    result = agent_executor.invoke({"input": query})
    print(result)