import nsg_audit_tool
import pytest

from nsg_audit_tool.cli import build_parser, main


def test_package_imports():
    assert nsg_audit_tool.__version__ == "0.1.0"


def test_build_parser_returns_parser():
    assert build_parser().prog == "nsg-audit"


def test_version_flag_prints_and_exits_zero(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["--version"])
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "nsg-audit-tool 0.1.0" in captured.out


@pytest.mark.parametrize("fmt", ["json", "csv", "markdown"])
def test_output_format_accepts_valid_choices(fmt, capsys):
    main(["--output-format", fmt])
    assert f"Selected output format: {fmt}" in capsys.readouterr().out


def test_output_format_defaults_to_json(capsys):
    main([])
    assert "Selected output format: json" in capsys.readouterr().out


def test_output_format_rejects_invalid_choice(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["--output-format", "yaml"])
    assert exc_info.value.code == 2
    assert "invalid choice" in capsys.readouterr().err
