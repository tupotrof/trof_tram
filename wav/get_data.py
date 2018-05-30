head_size = 44
encode_head_size = 12
encoding_code = b"TROFCODE"


def get_metadata(wav_raw):

    form = int.from_bytes(wav_raw[20:22], 'little')
    num_channels = int.from_bytes(wav_raw[22:24], 'little')
    sample_rate = int.from_bytes(wav_raw[24:28], 'little')
    bits_per_sample = int.from_bytes(wav_raw[34:36], 'little')

    return form, num_channels, sample_rate, bits_per_sample


def get_bits(file_raw):
    bits = []
    for byte in file_raw:
        bits.append(bool(byte & 128)),
        bits.append(bool(byte & 64)),
        bits.append(bool(byte & 32)),
        bits.append(bool(byte & 16)),
        bits.append(bool(byte & 8)),
        bits.append(bool(byte & 4)),
        bits.append(bool(byte & 2)),
        bits.append(bool(byte & 1)),
    return bits


def get_bytes(bits):
    bt = bytearray()
    for i in range(7, len(bits), 8):
        n = bits[i - 7] * 128 | bits[i - 6] * 64 | bits[i - 5] * 32 | bits[
            i - 4] * 16 \
            | bits[i - 3] * 8 | bits[i - 2] * 4 | bits[i - 1] * 2 | bits[i]
        bt.append(n)
    return bt
