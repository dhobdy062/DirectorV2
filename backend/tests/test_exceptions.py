import sys
sys.path.append('backend')

from director.utils.exceptions import DirectorException, AgentException, ToolException


def test_director_exception():
    exc = DirectorException("msg")
    assert str(exc) == "msg"


def test_agent_exception():
    exc = AgentException("agent err")
    assert str(exc) == "agent err"
    assert isinstance(exc, DirectorException)


def test_tool_exception():
    exc = ToolException("tool err")
    assert str(exc) == "tool err"
    assert isinstance(exc, DirectorException)
