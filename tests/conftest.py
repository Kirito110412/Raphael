import pytest
import json

@pytest.fixture
def mock_llm_response():
    with open("tests/fixtures/mock_llm_responses.json", "r") as f:
        return json.load(f)

@pytest.fixture
def temp_vault_dir(tmp_path):
    return tmp_path / "vault"

@pytest.fixture
def clean_l2_index():
    pass

@pytest.fixture
def reset_user_md():
    pass
