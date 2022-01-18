"""Satis AF-5 reader."""
import sys
from optparse import OptionParser  # pylint: disable=deprecated-module
import websocket

from satis import MAX_START, MAX_END, Rbw, Attenuation, sweep, read


class Command:
    """App commands."""

    Read = "read"
    Sweep = "sweep"


def cmd_read(socket, options):
    """App command read."""
    read(
      socket,
      options.freq_start,
      options.freq_end,
      int(options.rbw),
      options.video,
      int(options.atten),
      options.with_data
    )


def cmd_sweep(socket, options):
    """App command sweep."""
    print(sweep(
      socket,
      options.freq_center,
      int(options.rbw),
      options.video,
      int(options.atten)
    ))


COMMANDS = {
  Command.Read: cmd_read,
  Command.Sweep: cmd_sweep,
}

RBW = [str(i) for i in [
  Rbw.Hz6400,
  Rbw.Hz1600,
  Rbw.Hz400,
  Rbw.Hz100,
  Rbw.Hz25,
]]

ATTEN = [str(i) for i in [
  Attenuation.Db0,
  Attenuation.Db5,
  Attenuation.Db10,
  Attenuation.Db16,
  Attenuation.Db21,
  Attenuation.Db26,
  Attenuation.Db31,
]]

VERSION = '1.0'
USAGE = "%prog " + ' '.join(["[{}]".format(i) for i in COMMANDS])

PARSER = OptionParser(
  usage=USAGE,
  version="%prog version {}".format(VERSION)
)

PARSER.add_option(
  "--address",
  dest="address",
  default="192.168.1.100",
  help="Set satis websocket address. Default 192.168.1.100"
)
PARSER.add_option(
  "--with_data",
  action="store_true",
  dest="with_data",
  default=False,
  help="Dump received data."
)
PARSER.add_option(
  "--freq_center",
  type="int",
  dest="freq_center",
  default=MAX_START,
  help="Central frequency. Default is {}".format(MAX_START)
)
PARSER.add_option(
  "--freq_start",
  type="int",
  dest="freq_start",
  default=MAX_START,
  help="Start frequency. Default is {}".format(MAX_START)
)
PARSER.add_option(
  "--freq_end",
  type="int",
  dest="freq_end",
  default=MAX_END,
  help="End frequency. Default is {}".format(MAX_END)
)
PARSER.add_option(
  "--video",
  type="float",
  dest="video",
  default=100,
  help="End frequency. Default is 100"
)
PARSER.add_option(
  "--rbw",
  type="choice",
  choices=RBW,
  default=str(Rbw.Hz400),
  dest="rbw",
  help="Set rbw: %s. Default: %s" % (', '.join(RBW), Rbw.Hz400)
)
PARSER.add_option(
  "--atten",
  type="choice",
  choices=RBW,
  default=str(Attenuation.Db0),
  dest="atten",
  help="Set attenuation: %s. Default: %s" % (', '.join(ATTEN), Attenuation.Db0)
)


def main(argv, options):
    """Entry point."""
    print("Satis read utility v.{}.".format(VERSION))
    if len(argv) != 1:
        PARSER.print_usage()
        return 1

    cmd = argv[0]
    if cmd not in COMMANDS:
        PARSER.print_usage()
        return 1

    socket = websocket.WebSocket()
    socket.connect("ws://{}:8080".format(options.address))
    COMMANDS[cmd](socket, options)
    socket.close()
    return 0


if __name__ == '__main__':  # pragma: no cover
    OPTS, ARGS = PARSER.parse_args()
    sys.exit(main(ARGS, OPTS))
