"""FANUC-style G-code parser."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class GCodeCommand:
    block_number: Optional[int] = None
    g_codes: List[int] = None
    m_codes: List[int] = None
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None
    f: Optional[float] = None
    s: Optional[float] = None
    t: Optional[int] = None
    i: Optional[float] = None
    j: Optional[float] = None
    k: Optional[float] = None
    comment: Optional[str] = None

    def __post_init__(self) -> None:
        if self.g_codes is None:
            self.g_codes = []
        if self.m_codes is None:
            self.m_codes = []


class GCodeParser:
    """Parse FANUC-style G-code lines into structured commands."""

    _token_re = re.compile(r"([A-Z])([-+]?\d*\.?\d+)")
    _comment_re = re.compile(r"\(([^)]*)\)")

    def parse_line(self, line: str) -> GCodeCommand:
        line = line.strip().upper()
        comment = None
        comment_match = self._comment_re.search(line)
        if comment_match:
            comment = comment_match.group(1)
            line = self._comment_re.sub("", line).strip()

        cmd = GCodeCommand(comment=comment)

        if not line:
            return cmd

        for token in line.split():
            if token.startswith("N"):
                try:
                    cmd.block_number = int(token[1:])
                except ValueError:
                    continue
                continue

            match = self._token_re.match(token)
            if not match:
                continue

            letter, value = match.groups()
            num = float(value)

            if letter == "G":
                cmd.g_codes.append(int(num))
            elif letter == "M":
                cmd.m_codes.append(int(num))
            elif letter == "X":
                cmd.x = num
            elif letter == "Y":
                cmd.y = num
            elif letter == "Z":
                cmd.z = num
            elif letter == "F":
                cmd.f = num
            elif letter == "S":
                cmd.s = num
            elif letter == "T":
                cmd.t = int(num)
            elif letter == "I":
                cmd.i = num
            elif letter == "J":
                cmd.j = num
            elif letter == "K":
                cmd.k = num

        return cmd
