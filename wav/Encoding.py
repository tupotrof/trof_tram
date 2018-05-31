from . import get_data


def encode(wav, dest, text):
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
    print(sample_rate/1000, "kHz")
    print("Size:", numbytes, "bytes", "Time:",
          numbytes*8/bits_per_sample/sample_rate/num_channels)
    effective_size = int(numbytes / bits_per_sample) - get_data.encode_head_size
    print("Can encode", effective_size, "bytes")

    f = open(text, "rb")
    code_raw = f.read()
    f.close()

    code_size = len(code_raw)

    if code_size > effective_size:
        print("Error: file", text, "is too big to encode in", wav)
        print(code_size, ">", effective_size)
        return

    print(text, "-", code_size, "bytes")

    code_raw = get_data.encoding_code + code_size.to_bytes(4,
                                                           'little') + code_raw

    code_bits_bool = get_data.get_bits(code_raw)
    bytes_in_sample = bits_per_sample // 8

    for bit_number in range(0, len(code_bits_bool)):
        b = wav_raw[get_data.head_size + bit_number * bytes_in_sample]
        if code_bits_bool[bit_number]:
            wav_raw[get_data.head_size + bit_number * bytes_in_sample] \
                = (b // 2) * 2 + 1
        else:
            wav_raw[get_data.head_size + bit_number * bytes_in_sample] \
                = (b // 2) * 2

    f = open(dest, "wb")
    f.write(wav_raw)
    f.close()
    print("Encoded WAV saved to", dest)
