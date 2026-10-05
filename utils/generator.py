import asyncio
import io
import qrcode

def _build_image(data: str) -> bytes:
    img = qrcode.make(data, error_correction=qrcode.constants.ERROR_CORRECT_H)
    bfr = io.BytesIO()
    img.save(bfr, format="PNG")
    return bfr.getvalue()

async def generate_qr(data: str) -> bytes:
    return await asyncio.to_thread(_build_image, data)