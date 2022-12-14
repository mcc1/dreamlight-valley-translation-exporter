import os
import re
from pathlib import Path

# from . import decode_length

exp = re.compile(r"\"(.+?)\", \"(.+?)\"$", re.MULTILINE | re.UNICODE | re.DOTALL)


def encode_length(l: int) -> bytes:
    result = bytearray()

    while True:
        if (l // 128) == 0:
            result.append(l % 128)
            break
        result.append(l % 128 + 128)
        l = l // 128
    return result


def encode_data(key: str, val: str) -> bytes:
    # 0A total_len 0A key_len key 12 val_len val
    result = bytearray(b"\x0a")
    key_len = len(key.encode("utf8"))
    enc_key_len = encode_length(key_len)
    val_len = len(val.encode("utf8"))
    enc_val_len = encode_length(val_len)
    total_len = key_len + val_len
    if len(key) > 0:
        total_len += len(enc_key_len) + 1
    if len(val) > 0:
        total_len += len(enc_val_len) + 1
    result.extend(encode_length(total_len))
    if len(key) > 0:
        result.extend(b"\x0a" + enc_key_len + key.encode("utf8"))
    if len(val) > 0:
        result.extend(b"\x12" + enc_val_len + val.encode("utf8"))
    return result


def encode_file(input_file: Path, output_location=None):
    with open(input_file, encoding="utf8") as fp:
        if output_location is not None:
            if not output_location.parent.exists():
                os.makedirs(output_location.parent)
            wp = open(output_location.with_suffix(".locbin"), "wb")
        tmpline = ""
        lines = fp.readlines()
        for line in lines:
            if (data := exp.match(line)) is not None:
                key = data.group(1)
                val = data.group(2)
                wp.write(encode_data(key, val))
            else:
                tmpline += line
                if (data := exp.match(tmpline)) is not None:
                    tmpline = ""
                    key = data.group(1)
                    val = data.group(2)
                    wp.write(encode_data(key, val))
        if wp is not None:
            wp.close()


def zip_translation_pack(filepath: str, outputfile: str = 'LocDB_zh-CN.zip'):
    import zipfile
    # hardlink toturial.locbin from src folder
    filepath = Path(filepath)
    # if Path('src/tutorial.locbin').exists() and not (tmp := filepath / 'tutorial.locbin').exists():
    #     tmp.hardlink_to('src/tutorial.locbin')

    with zipfile.ZipFile(outputfile, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in filepath.glob('**/*.locbin'):
            zf.write(path, arcname=path.relative_to(filepath))


if __name__ == "__main__":
    for path in Path("working").glob("**/*.txt"):
        encode_file(path, "temp" / path.relative_to("./working"))

    zip_translation_pack("temp")
