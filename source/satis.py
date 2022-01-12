"""Satis AF-5 spectrum analizer stuff.

https://t.me/c/1160771584/109
"""
import json

FLD_REQUEST = "requestId"
FLD_START = "fStart"
FLD_END = "fEnd"
FLD_VIDEO = "video"
FLD_TOTAL_POINTS = "totalFreqPointsInChart"
FLD_FIRST_INDEX = "frameFirstPointIndex"
FLD_DATA = "data"
FLD_ALIVE = "alive"
FLD_ISALIVE = "spectrumAnaliserIsAlive"

MAX_START = 950000000
MAX_END = 2150000000


class Rbw:
    """Frequency step."""

    name = "rbw"

    Hz6400 = 0
    Hz1600 = 1
    Hz400 = 2
    Hz100 = 3
    Hz25 = 4


class Attenuation:
    """Attenuation of input signal."""

    name = "atten"

    Db0 = 0
    Db5 = 1
    Db10 = 2
    Db16 = 3
    Db21 = 4
    Db26 = 5
    Db31 = 6


class Mode:
    """Operation mode."""

    name = "mode"

    Stop = 0
    Cycle = 1
    Single = 2


CMD_ALIVE = {FLD_ALIVE: True}
CMD_STOP = {Mode.name: Mode.Stop}


def get_string(data):
    """Convert data dict to valid json string."""
    return ''.join(json.dumps(data).split())


def read(socket, freq_start, freq_end, rbw, video, atten):
    """Return list of satis data."""
    socket.send(get_string({
      FLD_REQUEST: 5,
      FLD_START: freq_start,
      FLD_END: freq_end,
      Rbw.name: rbw,
      FLD_VIDEO: video,
      Attenuation.name: atten,
      Mode.name: Mode.Single,
    }))

    result = json.loads(socket.recv())
    total = result[FLD_TOTAL_POINTS]
    data = result[FLD_DATA]
    count = len(data)

    while count < total:
        result = json.loads(socket.recv())
        if result[FLD_FIRST_INDEX] != count:
            raise Exception("Error: index {} count {}". format(result[FLD_FIRST_INDEX], count))

        data += result[FLD_DATA]
        count = len(data)

    return data
