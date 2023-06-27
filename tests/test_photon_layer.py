import base64
import io

from photon_observer import CommandType, PhotonLayer


def test_basic():
    # fmt: off
    photon_header = [
        0x00, 0x01,  # PeerID
        0x01,  # CrcEnabled
        0x01,  # CommandCount
        0x00, 0x00, 0x00, 0x01,  # Timestamp
        0x00, 0x00, 0x00, 0x01,  # Challenge
    ]
    photon_command = [
        CommandType.AcknowledgeType,  # Type
        0x01,  # ChannelID
        0x01,  # Flags
        0x04,  # ReservedByte
        0x00, 0x00, 0x00, 0x0c,  # Length
        0x00, 0x00, 0x00, 0x01,  # ReliableSequenceNumber
    ]
    # fmt: on
    data = bytes(photon_header + photon_command)
    print(data)
    packet = PhotonLayer.unpack(io.BytesIO(data))
    assert packet == {
        "challenge": 1,
        "command_count": 1,
        "commands": [
            {
                "channel_id": 1,
                "data": b"",
                "flags": 1,
                "length": 12,
                "reliable_sequence_number": 1,
                "reserved_byte": 4,
                "type": 1,
            }
        ],
        "contents": b"",
        "crc_enabled": 1,
        "payload": b"",
        "peer_id": 1,
        "timestamp": 1,
    }


def test_login_photon_layer():
    data = base64.b64decode(
        b"AAAABLNNdLV46INyBgABAAAAAL0AAAEO8wQBABMAYhABeAAAABDRivQ5Z2OeRKHySYvxxnvBAmI0A3MAJUhJR0hMQU5EX0dSRUVOX01BUktFVFBMQUNFX0NFTlRFUkNJVFkEeQACZr+AAABC2AAACHMABlN5c3RlbQlzAAZTeXN0ZW0NbwEQaQAPQkARbAjW98SV7KgKEmsnEBNsCNb4kxqcYNwUa///FWwI1viTGpxg3BdsCNb4kxqcYNwbbwEcbwEeYgD8awAhBgABAAAAABgAAAEP8wQBAAIAYmT8awEpBgABAAAAAEQAAAEQ8wQBAAkAaQAL+ysBawcsAmIBA3MACU1pc3RpY01hbgRiAQVpBycOAAZ4AAAAAAd4AAAAAPxrABkGAAEAAAADLwAAARHzAwEAACoAQgBpAAv7KgF4AAAAEOPXhPqnUIJLl18ny9qk/KUCcwAJTXlQaWNrbGUzA2IEBngAAAAFAAABAgIHeAAAAAUAAwAAAwhzAAQwMDA3CXkAAmZAwMmOQpe/ugpmQ0PH4AtmRJYAAAxmRJYAAA1mQUAAAA5sCNb5Jscux3MPZkLwAAAQZkLwAAARZj/AAAASbAjW+SbHLsdzE2ZEJ0AAFGZEJ0AAFWZA1hR7FmwI1vkmxy7HcxdmRupgABhmRupgABpsCNV73KAZ8zAcbAAAAACe1CuEHWwAAAAAAHoSAB5sAAAAADt3ipAfbAAAAAAAkPVgIGwI1XvcoBnzMCFsAAAAAlQLvPAibAAAAAAAAAAAJGwI1vkmxy7HcyV5AAVsAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACZiBCdzAA92ZXRlcmFuLWZvdW5kZXIocwAPdmV0ZXJhbi1zdGFydGVyKWIAKm8BK3gAAAAQcvpx3aSzQU6SEMkyFwhqZSx5AAppAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAL+ysAAAAAAAAAAC54AAAAEDfDLWHraw5InufShSBq9m8veAAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAxYgA0eQACZgAAAAAAAAAANnMABDAwMDA4eQACZgAAAAAAAAAAOnMAUTk2NzdkMDk2LTc1NDYtNGYzYi1iYmM3LWIwYjQ4OTVhYTcxM0BASVNMQU5EQDBhODY0ZmQxLTM3NTAtNDkyOC1iMDVlLTNmZDhjMGJmNjExZDtsCNb5Jscux3M8abNNdLVEcwAARnMAAEhsAAAAAAEwt9BLcwAATGwI1XvcoBnzME1iHk94AAAAAFB5AABsUXgAAAAAU28BVmwI1vkmoPR0+ldsCNb5JscvPM5YYgFZRGlsAABaeQAFbAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABbbAAAAAAAAAAA/WsAAg=="
    )
    packet = PhotonLayer.unpack(io.BytesIO(data))
    assert packet.command_count == 4
    assert len(packet.commands) == 4
    command = packet.commands[3]

    assert command.type == CommandType.SendReliableType
    assert command.length == 815

    msg = command.reliable_message()
    params = msg.decode()
    assert params[253] == 2
