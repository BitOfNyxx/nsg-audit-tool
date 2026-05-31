from dataclasses import dataclass

from nsg_audit_tool.checks import is_internet_exposed_sensitive_port


@dataclass
class FakeRule:
    direction: str = "Inbound"
    access: str | None = "Allow"
    source_address_prefix: str | None = None
    source_address_prefixes: list[str] | None = None
    destination_port_range: str | None = None
    destination_port_ranges: list[str] | None = None


def test_inbound_ssh_from_internet_is_flagged():
    rule = FakeRule(
        source_address_prefix="0.0.0.0/0",
        destination_port_range="22",
    )
    result = is_internet_exposed_sensitive_port(rule)
    assert result is True


def test_inbound_rdp_from_wildcard_source_is_flagged():
    rule = FakeRule(
        source_address_prefix="*",
        destination_port_range="3389",
    )
    result = is_internet_exposed_sensitive_port(rule)
    assert result is True


def test_non_sensitive_port_from_internet_not_flagged():
    rule = FakeRule(
        source_address_prefix="*",
        destination_port_range="25",
    )
    result = is_internet_exposed_sensitive_port(rule)
    assert result is False


def test_outbound_rule_to_sensitive_port_not_flagged():
    rule = FakeRule(
        direction="Outbound",
        source_address_prefix="0.0.0.0/0",
        destination_port_range="22",
    )
    result = is_internet_exposed_sensitive_port(rule)
    assert result is False


def test_deny_rule_on_sensitive_port_not_flagged():
    rule = FakeRule(
        access="Deny",
        source_address_prefix="Internet",
        destination_port_ranges=["22", "3389"],
    )
    result = is_internet_exposed_sensitive_port(rule)
    assert result is False


def test_specific_ip_source_to_sensitive_port_not_flagged():
    rule = FakeRule(source_address_prefix="192.168.1.1", destination_port_range="3389")
    result = is_internet_exposed_sensitive_port(rule)
    assert result is False


def test_rule_with_no_source_or_port_not_flagged():
    rule = FakeRule()
    result = is_internet_exposed_sensitive_port(rule)
    assert result is False
