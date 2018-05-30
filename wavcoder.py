import sys
import getopt

#from Help import help
from Decoding import decode
from Encoding import encode

def help():
    print("Usage: ./wavcoder -h")
    print("  display this help and exit")
    print("Usage: ./wavcoder -e <source> <code> <encode>")
    print("  encodes WAV file <source> of file <code>, result in <encode>")
    print("Usage: ./wavcoder -d <encode> <code>")
    print("  decodes WAV file <encode> to file <code>")

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def work(option, args):
    if option == '-h':
        help()
    elif option == '-d':
        wav = args[0]
        dest = args[1]
        decode(wav, dest)
    elif option == '-e':
        wav = args[0]
        dest = args[1]
        text = args[2]
        encode(wav, dest, text)
    else:
        raise Usage(AttributeError)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hde",
                                       ["help", "decode", "encode"])
            work(opts[0][0], args)
        except getopt.error as msg:
            raise Usage(msg)

    except Usage as err:
        print(err.msg)
        print("for help use -h")
        return 2


if __name__ == "__main__":
    sys.exit(main())
