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

use strict;

weechat::register('osc_notify', 'Benjamin Richter <br@waldteufel.eu>', '0.1', 'GPL3', 'use custom OSC codes to show remote notifications and play sounds', '', '');
weechat::hook_print('', 'irc_privmsg', '', 1, 'notify', '');

sub osc {
	print STDERR "\ePtmux;\e" if defined $ENV{TMUX};
	print STDERR "\e]777;".join(';',@_)."\a";
	print STDERR "\e\\" if defined $ENV{TMUX};
}

sub notify {
	my (undef, $buffer, $date, $tags, $displayed, $highlight, $prefix, $message) = @_;
	return unless $displayed;

	my %tags = map { $_ => 1 } split(',', $tags);

	if ($highlight || $tags{'notify_private'}) {
		print STDERR "\a";
		my $visible = weechat::window_search_with_buffer($buffer) eq weechat::current_window();
		osc 'im-notify', $visible, $prefix;
	}

	return weechat::WEECHAT_RC_OK;
}
