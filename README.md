# roku

Simple script with crappy ASCII-ish menu for numeric keypads to manage roku.

Works great for me.  Give it a shot and let me know what your take is.

# Usage

Pretty straight-forward

```
# Exmaple
$ rokuremote.py ROKU
# Connect by IP
$ rokuremote.py 192.168.0.101
# Connect by hostname
$ rokuremote.py np31313123burbleburble.domain
```

Behold the output:
```
You want to primarily use the numeric keypad but it's your choice.

|-------|-------|-------|-------|
|       |   /   |   -   |   *   |       Other keys:
|       |       | Volume| INFO  |
|       | SEARCH| Down  |       |       Key => Action
|-------|-------|-------|-------|       ---------------------------------
|   7   |   8   |   9   |   +   |       S   => Send a string
|  <--  |   ^   |   @   | Volume|       l   => List applications
| BACK  |  UP   | HOME  | Up    |       L   => Launch application
|-------|-------|-------|       |       I   => Install application
|   4   |   5   |   6   |       |       q   => Quit
|   <   |   OK  |   >   |       |       _   => VolumeMute (underscore)
| LEFT  | SELECT| RIGHT |       |
|-------|-------|-------|-------|
|   1   |   2   |   3   |       |
|  <<   |   \/  |   >>  | Enter |
| REWIND| DOWN  | F-FWD |       |
|-------|-------|-------|   or  |
|       0       |   .   |       |
|     |> / ||   |  <<-  | Return|
|  PLAY / PAUSE | REPLAY|       |
|---------------|-------|-------|

Please enter a key: 

```

# To-do

* Discover existing Roku's on network
* Prefer curses style layout but don't exactly know the best approach - suggestions welcome
* Create a class instead perhaps albeit it doesn't matter much
* Make it possibly web page friendly so I don't have to worry about it being pretty.
