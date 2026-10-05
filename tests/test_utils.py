import io
import pytest
from PIL import Image, ImageEnhance, ImageFilter
from utils.generator import generate_qr
from utils.reader import read_qr


# ==========================================
# 1. POSITIVE TESTS
# ==========================================

@pytest.mark.asyncio
async def test_full_cycle_simple_text():
    data = "1234567890005looool"
    qr_bytes = await generate_qr(data)
    result = await read_qr(qr_bytes)    
    assert result == data

@pytest.mark.asyncio
async def test_full_cycle_cyrillic_and_url():
    data = "https://example.com/test?param=Привет!"
    qr_bytes = await generate_qr(data)
    result = await read_qr(qr_bytes)
    assert result == data


@pytest.mark.asyncio
async def test_long_payload():
    data = "A" * 1000 
    qr_bytes = await generate_qr(data)
    result = await read_qr(qr_bytes)
    assert result == data

# ==========================================
# 2. NEGATIVE TESTS
# ==========================================

@pytest.mark.asyncio
async def test_corrupted_bytes():
    bad_bytes = b"this_is_not_a_photo_at_all_12345"
    result = await read_qr(bad_bytes)
    assert result is None


@pytest.mark.asyncio
async def test_image_without_qr():
    img = Image.new("RGB", (300, 300), color="red")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    result = await read_qr(buffer.getvalue())
    assert result is None


# ==========================================
# 3. ROBUSTNESS TESTS
# ==========================================

@pytest.mark.asyncio
@pytest.mark.parametrize("angle", [90, 180, 270, 45])
async def test_read_rotated_qr(angle: int):
    data = f"rotated_{angle}_deg"
    qr_bytes = await generate_qr(data)
    img = Image.open(io.BytesIO(qr_bytes))
    rotated_img = img.rotate(angle, expand=True)
    buffer = io.BytesIO()
    rotated_img.save(buffer, format="PNG")
    result = await read_qr(buffer.getvalue())
    assert result == data


@pytest.mark.asyncio
async def test_read_blurred_qr():
    data = "blurred_photo_test"
    qr_bytes = await generate_qr(data)
    img = Image.open(io.BytesIO(qr_bytes)).convert("RGB")
    blurred_img = img.filter(ImageFilter.GaussianBlur(radius=2))
    buffer = io.BytesIO()
    blurred_img.save(buffer, format="PNG")
    result = await read_qr(buffer.getvalue())
    assert result == data


@pytest.mark.asyncio
async def test_read_dark_qr():
    data = "dark_photo_test"
    qr_bytes = await generate_qr(data)
    img = Image.open(io.BytesIO(qr_bytes)).convert("RGB")
    enhancer = ImageEnhance.Brightness(img)
    dark_img = enhancer.enhance(0.3)
    buffer = io.BytesIO()
    dark_img.save(buffer, format="PNG")
    result = await read_qr(buffer.getvalue())
    assert result == data