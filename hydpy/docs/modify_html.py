# -*- coding: utf-8 -*-
"""Beautify the html documentation generated by `Sphinx`."""

import os
import sys
from typing import *

try:
    print("\nModify html files:")
    folder = os.path.join("hydpy", "docs", "auto", "build")
    paths = sorted(
        os.path.join(folder, fn) for fn in os.listdir(folder) if fn.endswith(".html")
    )
    for path in paths:
        path = os.path.abspath(path)
        print("  " + path)
        sys.stdout.flush()
        lines: List[str] = []
        with open(path, encoding="utf-8-sig") as file_:
            for line in file_.readlines():
                if line.startswith("<dd><p>alias of <a " 'class="reference external"'):
                    line = line.split("span")[1]
                    line = line.split(">")[1]
                    line = line.split("<")[0]
                    lines[-1] = lines[-1].replace(
                        "TYPE</code>",
                        f'TYPE</code><em class="property"> = {line}</em>',
                    )
                else:
                    lines.append(line)
        text = "".join(lines)
        with open(path, "w", encoding="utf-8-sig") as file_:
            file_.write(text)
except BaseException as exc:
    print(exc)
    sys.exit(1)
else:
    sys.exit(0)
