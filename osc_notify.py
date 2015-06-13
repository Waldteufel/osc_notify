# use custom OSC codes to show remote notifications and play sounds

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import weechat

import os
import sys
import subprocess

weechat.register('osc_notify', 'Benjamin Richter <br@waldteufel.eu>', '0.2', 'GPL3', 'use custom OSC codes to show remote notifications and play sounds', '', '')
weechat.hook_print('', 'irc_privmsg', '', 1, 'osc_notify_hook', '')

def is_tmux_visible():
    if os.getenv('TMUX') is None: return True
    else: return subprocess.check_output(['tmux', 'display-message', '-p', '#{pane_id}']).strip() == os.getenv('TMUX_PANE')

def send_osc(*args):
    msg = "\a\x1b]777;" + ';'.join(str(x) for x in args) + "\a";

    if os.getenv('TMUX'):
        clients = subprocess.check_output(['tmux', 'list-clients', '-F', '#{client_tty} #{client_termname}']).strip()
        if clients:
            for line in clients.split('\n'):
                tty, term = line.split()
                if term.startswith('rxvt'):
                    with open(tty, 'w') as f:
                        f.write(msg)
    elif os.getenv('TERM').startswith('rxvt'):
        sys.stderr.write(msg)

def osc_notify_hook(udata, buf, date, tags, displayed, highlight, prefix, message):
    if displayed and (highlight or 'notify_private' in tags.split(',')):
        is_visible = weechat.window_search_with_buffer(buf) == weechat.current_window()
        send_osc('im-notify', int(is_visible), int(is_tmux_visible()), prefix)

    return weechat.WEECHAT_RC_OK
