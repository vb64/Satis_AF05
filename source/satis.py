"""Satis AF-5 spectrum analizer stuff."""
import json

MAX_START = 950000000
MAX_END = 2150000000


class Error(Exception):
    """Satis IO exception."""


class Key:
    """Keys for satis json IO."""

    Request = "requestId"
    Start = "fStart"
    End = "fEnd"
    Video = "video"
    Total = "totalFreqPointsInChart"
    First = "frameFirstPointIndex"
    Data = "data"
    Alive = "alive"
    Is_alive = "spectrumAnaliserIsAlive"

    # sweep mode keys
    VideoSweep = "dataFreq"  # from 1 to 20
    Center = "fCentral"  # from MAX_START to MAX_END
    MaxFreq = "maximumFreq"
    MaxVal = "maximumValue"
    Time = "timeStamp"  # milliseconds from last request


class Rbw:
    """Frequency step."""

    name = "rbw"

    Hz6400 = 0
    Hz1600 = 1
    Hz400 = 2
    Hz100 = 3
    Hz25 = 4


class RbwSweep:
    """Frequency step for sweep mode."""

    name = "rbwsweep"

    Hz6400 = 0
    Hz1600 = 1
    Hz400 = 2


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
    Sweep = 3


CMD_ALIVE = {Key.Alive: True}
CMD_STOP = {Mode.name: Mode.Stop}


def get_string(data):
    """Convert data dict to valid json string."""
    return ''.join(json.dumps(data).split())


def sweep(socket, freq, rbw, video, atten):
    """Return data in sweep mode."""
    socket.send(get_string({
      Key.Request: 6,
      Key.Center: freq,
      Rbw.name: rbw,
      Key.VideoSweep: video,
      Attenuation.name: atten,
      Mode.name: Mode.Sweep,
    }))

    return json.loads(socket.recv())


def dump(result, with_data):
    """Print json data."""
    if not with_data:
        result[Key.Data] = len(result[Key.Data])
    print(result)


def read(socket, freq_start, freq_end, rbw, video, atten, with_data):
    """Return list of satis data."""
    socket.send(get_string({
      Key.Request: 5,
      Key.Start: freq_start,
      Key.End: freq_end,
      Rbw.name: rbw,
      Key.Video: video,
      Attenuation.name: atten,
      Mode.name: Mode.Single,
    }))

    result = json.loads(socket.recv())
    total = result[Key.Total]
    data = result[Key.Data]
    count = len(data)
    dump(result, with_data)

    while count < total:
        result = json.loads(socket.recv())
        if result[Key.First] != count:
            raise Error("Error: index {} count {}". format(result[Key.First], count))

        dump(result, with_data)
        count += len(data)

    return count
