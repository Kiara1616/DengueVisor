from pathlib import Path
from streamlit.testing.v1 import AppTest

def test_app_themes_and_empty_search():
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py")).run(timeout=30)
    assert not app.exception
    app.toggle[0].set_value(True).run()
    assert not app.exception
    app.text_input[0].set_value("NO_EXISTE").run()
    assert not app.exception
    assert app.info
