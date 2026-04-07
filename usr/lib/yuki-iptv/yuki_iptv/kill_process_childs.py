#
# Copyright (c) 2021, 2022 Astroncia
# Copyright (c) 2023-2025 liya <liyaliya@tutamail.com>
#
# This file is part of yuki-iptv.
#
# yuki-iptv is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# yuki-iptv is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with yuki-iptv. If not, see <https://www.gnu.org/licenses/>.
#
# The Font Awesome pictograms are licensed under the CC BY 4.0 License.
# Font Awesome Free 5.15.4 by @fontawesome - https://fontawesome.com
# https://creativecommons.org/licenses/by/4.0/
#
import os
import sys
import signal
import logging
import subprocess

logger = logging.getLogger(__name__)


def _get_pid(proc):
    try:
        return proc.processId()
    except AttributeError:
        return int(proc)


def kill_process_childs(proc):
    try:
        pid = _get_pid(proc)
        if sys.platform == "win32":
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(pid)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:
            child_process_ids = [
                int(line)
                for line in subprocess.run(
                    [
                        "ps",
                        "-opid",
                        "--no-headers",
                        "--ppid",
                        str(pid),
                    ],
                    stdout=subprocess.PIPE,
                    encoding="utf8",
                ).stdout.splitlines()
            ]
            for child_process_id in child_process_ids:
                logger.info(f"Terminating process with PID {child_process_id}")
                os.kill(child_process_id, signal.SIGKILL)
    except Exception:
        pass
