from photon_observer import FragmentBuffer, ReliableFragment


def test_fragment_buffer():
    buffer = FragmentBuffer()

    f1 = ReliableFragment(
        sequence_number=7,
        fragment_number=0,
        fragment_count=2,
        total_length=2,
        fragment_offset=0,
        data=b"\xca",
    )
    f2 = ReliableFragment(
        sequence_number=7,
        fragment_number=1,
        fragment_count=2,
        total_length=2,
        fragment_offset=0,
        data=b"\xfe",
    )

    result = buffer.offer(f1)
    assert result is None

    result = buffer.offer(f2)
    assert result.data == b"\xca\xfe"
    assert result.reliable_sequence_number == 7
