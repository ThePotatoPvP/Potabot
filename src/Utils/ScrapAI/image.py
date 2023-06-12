from src.Utils.ScrapAI.imaginepy import AsyncImagine, Style, Ratio
import io

async def generate_image(image_prompt, style_value, ratio_value, negative, upscale):
    imagine = AsyncImagine()
    style_enum = Style[style_value]
    ratio_enum = Ratio[ratio_value]
    img_data = await imagine.sdprem(
        prompt=image_prompt,
        style=style_enum,
        ratio=ratio_enum,
        priority="1",
        high_res_results="1",
        steps="70",
        negative=negative
    )

    if upscale:
        img_data = await imagine.upscale(image=img_data)

    try:
        img_file = io.BytesIO(img_data)
    except Exception as e:
        print(
            f"An error occurred while creating the in-memory image file: {e}")
        return None

    await imagine.close()
    return img_file