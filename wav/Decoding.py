from . import get_data


def decode(wav, dest):
    f = open(wav, "rb")
    wav_raw = bytearray(f.read())
    f.close()

    form, num_channels, sample_rate, bits_per_sample \
        = get_data.get_metadata(wav_raw)

    if form != 1:
        print("Error in data type")
        return None

    numbytes = len(wav_raw) - get_data.head_size

    print(bits_per_sample, "BPS x", num_channels, "ch")
    print(sample_rate / 1000, "kHz")
    print("Size:", numbytes, "bytes", "Time:",
          numbytes * 8 / bits_per_sample / sample_rate / num_channels)

    bytes_in_sample = bits_per_sample // 8

    meta_bits = []
    meta_size = get_data.encode_head_size * 8
    for bit_number in range(0, meta_size):
        meta_bits.append(
            wav_raw[get_data.head_size + bit_number * bytes_in_sample] % 2 == 1)

    meta_raw = get_data.get_bytes(meta_bits)
    if meta_raw[:len(get_data.encoding_code)] != get_data.encoding_code:
        print("Nothing is decoded in file", wav)
        return

    file_size = int.from_bytes(meta_raw[len(get_data.encoding_code):], 'little')
    print("Detected encoded file, size =", file_size, "bytes")

    bits = []
    for bit_number in range(meta_size, file_size * 8 + meta_size):
        bits.append(
            wav_raw[get_data.head_size + bit_number * bytes_in_sample] % 2 == 1)

    file_raw = get_data.get_bytes(bits)

    f = open(dest, "wb")
    f.write(file_raw)
    f.close()
    print("File written to", dest)
