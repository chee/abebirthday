"""
The `wifi` module provides necessary low-level functionality for managing wifi
wifi connections. Use `socketpool` for communicating over the network."""

from __future__ import annotations

import ipaddress
from typing import Iterable, Iterator, Optional

from _typing import ReadableBuffer

radio: Radio
"""Wifi radio used to manage both station and AP modes.
This object is the sole instance of `wifi.Radio`."""

class Network:
    """A wifi network provided by a nearby access point."""

    def __init__(self) -> None:
        """You cannot create an instance of `wifi.Network`. They are returned by `wifi.Radio.start_scanning_networks`."""
        ...
    ssid: str
    """String id of the network"""

    bssid: bytes
    """BSSID of the network (usually the AP's MAC address)"""

    rssi: int
    """Signal strength of the network"""

    channel: int
    """Channel number the network is operating on"""

class Radio:
    """Native wifi radio.

    This class manages the station and access point functionality of the native
    Wifi radio.

    """

    def __init__(self) -> None:
        """You cannot create an instance of `wifi.Radio`.
        Use `wifi.radio` to access the sole instance available."""
        ...
    enabled: bool
    """``True`` when the wifi radio is enabled.
    If you set the value to ``False``, any open sockets will be closed.
    """

    mac_address: bytes
    """MAC address of the wifi radio. (read-only)"""
    def start_scanning_networks(
        self, *, start_channel: int = 1, stop_channel: int = 11
    ) -> Iterable[Network]:
        """Scans for available wifi networks over the given channel range. Make sure the channels are allowed in your country."""
        ...
    def stop_scanning_networks(self) -> None:
        """Stop scanning for Wifi networks and free any resources used to do it."""
        ...
    hostname: ReadableBuffer
    """Hostname for wifi interface. When the hostname is altered after interface started/connected
       the changes would only be reflected once the interface restarts/reconnects."""
    def connect(
        self,
        ssid: ReadableBuffer,
        password: ReadableBuffer = b"",
        *,
        channel: Optional[int] = 0,
        bssid: Optional[ReadableBuffer] = b"",
        timeout: Optional[float] = None
    ) -> bool:
        """Connects to the given ssid and waits for an ip address. Reconnections are handled
        automatically once one connection succeeds.

        By default, this will scan all channels and connect to the access point (AP) with the
        given ``ssid`` and greatest signal strength (rssi).

        If ``channel`` is given, the scan will begin with the given channel and connect to
        the first AP with the given ``ssid``. This can speed up the connection time
        significantly because a full scan doesn't occur.

        If ``bssid`` is given, the scan will start at the first channel or the one given and
        connect to the AP with the given ``bssid`` and ``ssid``."""
        ...
    ipv4_gateway: Optional[ipaddress.IPv4Address]
    """IP v4 Address of the gateway when connected to an access point. None otherwise."""

    ipv4_subnet: Optional[ipaddress.IPv4Address]
    """IP v4 Address of the subnet when connected to an access point. None otherwise."""

    ipv4_address: Optional[ipaddress.IPv4Address]
    """IP v4 Address of the radio when connected to an access point. None otherwise."""

    ipv4_dns: Optional[ipaddress.IPv4Address]
    """IP v4 Address of the DNS server in use when connected to an access point. None otherwise."""

    ap_info: Optional[Network]
    """Network object containing BSSID, SSID, channel, and RSSI when connected to an access point. None otherwise."""
    def ping(
        self, ip: ipaddress.IPv4Address, *, timeout: Optional[float] = 0.5
    ) -> float:
        """Ping an IP to test connectivity. Returns echo time in seconds.
        Returns None when it times out."""
        ...

class ScannedNetworks:
    """Iterates over all `wifi.Network` objects found while scanning. This object is always created
    by a `wifi.Radio`: it has no user-visible constructor."""

    def __init__(self) -> None:
        """Cannot be instantiated directly. Use `wifi.Radio.start_scanning_networks`."""
        ...
    def __iter__(self) -> Iterator[Network]:
        """Returns itself since it is the iterator."""
        ...
    def __next__(self) -> Network:
        """Returns the next `wifi.Network`.
        Raises `StopIteration` if scanning is finished and no other results are available."""
        ...
