"""Satis AF-5 reader."""
import sys
from optparse import OptionParser  # pylint: disable=deprecated-module
import websocket

from satis import MAX_START, MAX_END, Rbw, RbwSweep, Attenuation, sweep, read


class Command:
    """App commands."""

    Read = "read"
    Sweep = "sweep"


def cmd_read(socket, options):
    """App command read."""
    print("Total points:", read(
      socket,
      options.freq_start,
      options.freq_end,
      int(options.rbw),
      options.video,
      int(options.atten),
      options.with_data
    ))


def cmd_sweep(socket, options):
    """App command sweep."""
    print(sweep(
      socket,
      options.freq_center,
      int(options.rbwsweep),
      options.datafreq,
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

RBW_SWEEP = [str(i) for i in [
  RbwSweep.Hz6400,
  RbwSweep.Hz1600,
  RbwSweep.Hz400,
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
  default="192.168.0.100",
  help="Set satis websocket address. Default 192.168.0.100"
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
  help="Frequency of averaging the result over a period of time in hertz. From 0.1 to 6400. Default is 100"
)
PARSER.add_option(
  "--datafreq",
  type="float",
  dest="datafreq",
  default=10,
  help="Frequency of averaging the result over a period of time in hertz. From 1 to 20. Default is 10"
)
PARSER.add_option(
  "--rbw",
  type="choice",
  choices=RBW,
  default=str(Rbw.Hz400),
  dest="rbw",
  help="Set rbw for read dommand: %s. Default: %s" % (', '.join(RBW), Rbw.Hz400)
)
PARSER.add_option(
  "--rbwsweep",
  type="choice",
  choices=RBW_SWEEP,
  default=str(RbwSweep.Hz6400),
  dest="rbwsweep",
  help="Set rbw for sweep command: %s. Default: %s" % (', '.join(RBW_SWEEP), RbwSweep.Hz6400)
)
PARSER.add_option(
  "--atten",
  type="choice",
  choices=ATTEN,
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
