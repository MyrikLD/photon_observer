from photon_observer.photon_command import PhotonCommand
from photon_observer.enums import MessageType, CommandType, ReliableMessageType


def test_reliable_message_operation_response():
    cmd = PhotonCommand(
        type=CommandType.SendReliableType,
        channel_id=0,
        flags=0,
        reserved_byte=0,
        length=0,
        reliable_sequence_number=0,
        data=bytes(
            [
                0x00,
                MessageType.otherOperationResponse,
                0x01,
                0x00,
                0x01,
                ReliableMessageType.NilType,
                0x00,
                0x01,
                0x09,
                0x00,
            ]
        ),
    )
    msg = cmd.reliable_message()
    data = msg.decode()
    assert data == {9: None}
