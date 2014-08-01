export DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $DIR >> .iwatch.log
screen -S ipython_watch -c $DIR/ipython_watch_screenrc
