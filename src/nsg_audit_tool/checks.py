from typing import Protocol

# List of criteria (Ports/Public Sources)
SENSITIVE_PORTS = ["22", "3389"]
PUBLIC_SOURCES = {"0.0.0.0/0", "*", "Internet"}


# RuleLike Protocol
class RuleLike(Protocol):
    direction: str
    access: str | None
    source_address_prefix: str | None
    source_address_prefixes: list[str] | None
    destination_port_range: str | None
    destination_port_ranges: list[str] | None


def _all_sources(rule: RuleLike) -> list[str]:
    addresses = []
    if rule.source_address_prefix:
        addresses.append(rule.source_address_prefix)

    if rule.source_address_prefixes:
        addresses.extend(rule.source_address_prefixes)
    return addresses


def _all_destination_ports(rule: RuleLike) -> list[str]:
    ports = []
    if rule.destination_port_range:
        ports.append(rule.destination_port_range)

    if rule.destination_port_ranges:
        ports.extend(rule.destination_port_ranges)
    return ports


def _is_public_source(prefix: str) -> bool:
    return prefix in PUBLIC_SOURCES


def _allows_sensitive_ports(spec: str) -> bool:
    if spec == "*":
        return True

    # Split ranges into a list then perform range check against sensitive ports list
    if "-" in spec:
        start, end = spec.split("-")
        return any(int(start) <= int(port) <= int(end) for port in SENSITIVE_PORTS)
    return spec in SENSITIVE_PORTS


def is_internet_exposed_sensitive_port(rule: RuleLike) -> bool:
    # Only allows function to continue if direction and access are set correctly
    if rule.direction != "Inbound":
        return False
    if rule.access != "Allow":
        return False

    public_source = any(_is_public_source(s) for s in _all_sources(rule))
    sensitive_port = any(
        _allows_sensitive_ports(s) for s in _all_destination_ports(rule)
    )

    return public_source and sensitive_port
