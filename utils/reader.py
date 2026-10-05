import asyncio
import io
from PIL import Image
import zxingcpp


def _read_qr(image_bytes: bytes) -> str | None:
    try:
        img = Image.open(io.BytesIO(image_bytes))
    except:
        return None
    rslt = zxingcpp.read_barcodes(img)
    if rslt:
        return rslt[0].text
    return None

async def read_qr(image_bytes: bytes) -> str | None:
    return await asyncio.to_thread(_read_qr, image_bytes)
