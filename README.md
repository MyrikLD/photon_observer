# Photon Observer

Tools for working with the [Photon protocol](https://doc.photonengine.com/realtime/current/reference/binary-protocol).

### Example:
```python
import pyshark
import io
from photon_observer import PhotonLayer, FragmentBuffer, CommandType, ReliableMessage

def on_message(message: ReliableMessage):
    pass

def main():
    capture = pyshark.LiveCapture("wlp4s0", bpf_filter="udp")
    buf = FragmentBuffer()

    for p in capture.sniff_continuously():
        payload = bytes.fromhex(p.udp.payload.replace(":", ''))
        layer = PhotonLayer.unpack(io.BytesIO(payload))
        
        for cmd in layer.commands:
            if cmd.type == CommandType.SendReliableType:
                msg = cmd.reliable_message()
                on_message(msg)
            elif cmd.type == CommandType.SendUnreliableType:
                _cmd = cmd.unreliable_type()
                msg = _cmd.reliable_message()
                on_message(msg)
            elif cmd.type == CommandType.SendReliableFragmentType:
                msg = cmd.reliable_fragment()
                result = buf.offer(msg)
                if result is not None:
                    msg = result.reliable_message()
                    on_message(msg)
            else:
                continue
```

## PS
Additional thanks to @hmadison for his [photon_spectator](https://github.com/hmadison/photon_spectator) package

## License
This project is licensed under MIT. Contributions to this project are accepted under the same license. 
