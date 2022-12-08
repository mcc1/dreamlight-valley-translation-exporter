import os
from pathlib import Path


def decode_length(n: bytes) -> int:
    result = 0
    if len(n) < 1:
        raise ValueError("Invalid length")
    for i in range(1, len(n) + 1):
        result += (n[i - 1] - 1) * pow(128, i - 1)
    result += 1
    return result


def decode_data(kv: bytes) -> (str, str):
    key = val = b""
    key_length = val_length = 0
    key_bit = val_bit = 1

    key_pos = kv.find(b"\x0a")
    # check have key or not
    if key_pos != -1:
        # try to decode key_length
        while (l := decode_length(kv[key_pos + 1 : key_pos + 1 + key_bit])) < 5000:
            key_length = l
            key_bit += 1
        key_bit -= 1
        key = kv[key_pos + key_bit + 1 : key_pos + key_bit + key_length + 1]

    val_pos = kv.find(b"\x12", key_pos + key_bit + key_length)
    # check have val or not
    if val_pos != -1:
        # try to decode val_length
        while (l := decode_length(kv[val_pos + 1 : val_pos + 1 + val_bit])) < len(kv):
            val_length = l
            val_bit += 1
        val_bit -= 1
        val = kv[val_pos + val_bit + 1 : val_pos + val_bit + val_length + 1]
    # if key_length + key_bit + val_length + val_bit + 2 != len(kv):
    #     print(key_length, key_bit, val_length, val_bit, len(kv))
    #     raise ValueError("key value length mismatch")
    try:
        return key.decode("utf8"), val.decode("utf8")
    except Exception as e:
        print(key, val, e)
        return "Error", "Error"


def decode_file(input_file: Path, output_location=None):
    buffer_size = 10
    with open(input_file, "rb") as fp:
        if output_location is not None:
            if not output_location.parent.exists():
                os.makedirs(output_location.parent)
            wp = open(output_location.with_suffix(".txt"), "w+", encoding="utf8")
        while (header := fp.read(buffer_size)) != b"":
            total_meta_pos = header.index(b"\x0a")
            if (key_meta_pos := header.find(b"\x0a", total_meta_pos + 1)) == -1:
                # missing key
                key_meta_pos = header.find(b"\x12", total_meta_pos + 1)
            total_length = decode_length(header[total_meta_pos + 1 : key_meta_pos])
            # reset fp to key_meta_pos
            fp.seek(-(buffer_size - key_meta_pos), 1)
            key, val = decode_data(fp.read(total_length))
            if output_location == None:
                print(key, val)
            else:
                wp.write(f'"{key}", "{val}"\n')
        wp.close()


if __name__ == "__main__":
    for path in Path("./src").glob("**/*.locbin"):
        # if path.name == "tutorial.locbin":
        #     continue
        decode_file(path, "working" / path.relative_to("./src"))
