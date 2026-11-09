from on_device_private_agent import Document, PrivateAgent, TfidfIndex
from on_device_private_agent.planner import plan
from on_device_private_agent.retrieval import tokenize


def test_tokenize_filters_stopwords():
    assert "the" not in tokenize("the quick brown fox")
    assert "quick" in tokenize("the quick brown fox")

def test_retrieval_ranks_relevant_first():
    agent = PrivateAgent()
    hits = agent.index.search("inference cost zero dollars", k=2)
    assert hits and hits[0].doc.id in {"pricing", "privacy"}

def test_ask_is_free_and_offline():
    ans = PrivateAgent().ask("How does privacy work?")
    assert ans.cost_usd == 0.0 and ans.offline is True and ans.sources

def test_ask_no_match():
    ans = PrivateAgent().ask("zzzqqq nonexistentterm")
    assert "No matching" in ans.text

def test_planner_intents():
    assert plan("summarise quantization").action == "summarise"
    assert plan("list documents please").action == "list"
    assert plan("help").action == "help"
    assert plan("what is offline mode").action == "retrieve"

def test_summarise_and_list():
    agent = PrivateAgent()
    assert agent.ask("summarise quantization").intent == "summarise"
    listed = agent.ask("list documents")
    assert "Privacy model" in listed.text

def test_add_document():
    agent = PrivateAgent(docs=[Document("a", "Alpha", "alpha beta gamma unique")])
    agent.add_document(Document("b", "Beta", "delta epsilon zeta"))
    assert len(agent.index) == 2
    assert agent.index.search("delta epsilon")[0].doc.id == "b"

def test_index_empty_query():
    idx = TfidfIndex([Document("x", "X", "hello world")])
    assert idx.search("") == []


def test_cli_demo_e2e(capsys):
    from on_device_private_agent.cli import main
    assert main(["demo"]) == 0
    out = capsys.readouterr().out
    assert "cost=$0.0" in out and "privacy" in out.lower()


def test_config_from_env(monkeypatch):
    from on_device_private_agent.config import Settings
    monkeypatch.setenv("PRIVATE_AGENT_LOG_LEVEL", "DEBUG")
    assert Settings.from_env().log_level == "DEBUG"
