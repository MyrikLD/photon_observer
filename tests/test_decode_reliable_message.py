import io
import math

import pytest

from photon_observer.enums import ReliableMessageType, MessageType
from photon_observer.reliable_message import ReliableMessage

tests = [
    [
        [0x00, ReliableMessageType.Int8Type, 0xFF],
        {0: -1},
    ],
    [
        [0x00, ReliableMessageType.Float32Type, 0x43, 0x00, 0x20, 0xC5],
        {0: 128.128},
    ],
    [
        [0x00, ReliableMessageType.Int32Type, 0x00, 0x00, 0x00, 0x80],
        {0: 128},
    ],
    [
        [0x00, ReliableMessageType.Int16Type, 0x00, 0x80],
        {0: 128},
    ],
    [
        [
            0x00,
            ReliableMessageType.Int64Type,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x80,
        ],
        {0: 128},
    ],
    [
        [0x00, ReliableMessageType.StringType, 0x00, 0x03, 0x61, 0x62, 0x63],
        {0: "abc"},
    ],
    [
        [0x00, ReliableMessageType.BooleanType, 0x00],
        {0: False},
    ],
    [
        [0x00, ReliableMessageType.BooleanType, 0x01],
        {0: True},
    ],
    [
        [0x00, ReliableMessageType.Int8SliceType, 0x00, 0x00, 0x00, 0x01, 0x01],
        {0: [1]},
    ],
    [
        [
            0x00,
            ReliableMessageType.SliceType,
            0x00,
            0x01,
            ReliableMessageType.Float32Type,
            0x43,
            0x00,
            0x20,
            0xC5,
        ],
        {0: [128.128]},
    ],
    [
        [
            0x00,
            ReliableMessageType.SliceType,
            0x00,
            0x01,
            ReliableMessageType.Int32Type,
            0x00,
            0x00,
            0x00,
            0x80,
        ],
        {0: [128]},
    ],
    [
        [
            0x00,
            ReliableMessageType.SliceType,
            0x00,
            0x01,
            ReliableMessageType.Int16Type,
            0x00,
            0x80,
        ],
        {0: [128]},
    ],
    [
        [
            0x00,
            ReliableMessageType.SliceType,
            0x00,
            0x01,
            ReliableMessageType.Int64Type,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x80,
        ],
        {0: [128]},
    ],
    [
        [
            0x00,
            ReliableMessageType.SliceType,
            0x00,
            0x01,
            ReliableMessageType.StringType,
            0x00,
            0x03,
            0x61,
            0x62,
            0x63,
        ],
        {0: ["abc"]},
    ],
    [
        [
            0x00,
            ReliableMessageType.SliceType,
            0x00,
            0x01,
            ReliableMessageType.BooleanType,
            0x01,
        ],
        {0: [True]},
    ],
    [
        [
            0x00,
            ReliableMessageType.SliceType,
            0x00,
            0x01,
            ReliableMessageType.BooleanType,
            0x00,
        ],
        {0: [False]},
    ],
    [
        [
            0x00,
            ReliableMessageType.SliceType,
            0x00,
            0x01,
            ReliableMessageType.Int8SliceType,
            0x00,
            0x00,
            0x00,
            0x01,
            0x01,
        ],
        {0: [[1]]},
    ],
    [
        [
            0x00,
            ReliableMessageType.SliceType,
            0x00,
            0x01,
            ReliableMessageType.SliceType,
            0x00,
            0x01,
            ReliableMessageType.BooleanType,
            0x00,
        ],
        {0: [[False]]},
    ],
]


@pytest.mark.parametrize("msg,expected", tests)
def test_decode(msg, expected):
    msg = ReliableMessage(
        signature=0,
        type=MessageType.otherOperationResponse,
        paramater_count=1,
        data=bytes(msg),
    )
    assert msg.decode() == expected
