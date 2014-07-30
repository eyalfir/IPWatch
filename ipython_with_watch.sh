export DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
screen -S ipython_watch -c $DIR/ipython_watch_screenrc
