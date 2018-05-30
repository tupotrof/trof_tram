import sys
import getopt

from tram.stop_search import stop_s
from tram.help import get_help
from tram.route_search import route_s

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def work(option, args):
    if option == '-h':
        get_help()
    elif option == '-s':
        stop = args[0]
        stop_s(stop)
    elif option == '-r':
        route = args[0]
        route_s(route)

    else:
        raise Usage(AttributeError)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:],
                                       "hsr", ["help", "stop", "route"])
            print(opts)
            print(args)
            work(opts[0][0], args)
        except getopt.error as msg:
            raise Usage(msg)

    except Usage as err:
        print(sys.stderr, err.msg)
        print(sys.stderr, "for help use --help")
        return 2


if __name__ == "__main__":
    sys.exit(main())
