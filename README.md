OSC Notify
==========

Install the URxvt and weechat plugins and have desktop-notifications from
weechat even over SSH and from inside TMUX.


Usage
-----

The format of notification messages is as follows:

```$ printf "\e]777;im-notify;%d;%d;%s\a" 0 0 nick```

If the first argument is `1`, no notification sound is played. If the second
argument is `1`, no notification sound is played '''and''' no notification is
shown.
