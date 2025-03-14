import base64
from typing import List
from fastapi import UploadFile

from pictoroute.core.genai import claude_vision_response_with_json_response
from pictoroute.models.address import Address


PROMPT = """
You are an advanced AI system specialized in extracting and structuring address information from images of tables. Your task is to process Dutch addresses and output them in a structured JSON format.

First, examine the attached image(s) of address tables.

Your goal is to extract valid, complete addresses from these images and structure them according to the specified format. Follow these steps carefully:

1. Extract Cell Data:
- Identify each cell in the table.
- Extract the text content from each cell.
- If a cell's text spans multiple lines, concatenate them into a single string.

2. Address Parsing:
For each address, you need to identify and extract the following components:
- street_name: The name of the street, ensuring correct spelling (particularly for Dutch-specific names).
- house_number: The numeric identifier of the house, possibly with an alphabetic suffix.
- postal_code: In the format "1234AB" (without the house number attached).
- city: Extracted from the context.

3. Address Validation:
- Ensure each address is complete and valid.
- Verify that the house number appears twice: once in the street name and once after the postal code.
- Be strict in maintaining the order and correct spelling of elements as provided in the table cells.

4. Error Handling and Correction:
- Pay special attention to cases where the house number is repeated after the postal code (e.g., "1234AB84" where 1234AB is the postal code and 84 is the house number).
- If you encounter such cases, separate the house number from the postal code correctly.

For each address, wrap your thought process in <processing> tags using the following structure:

<processing>
Table Cell Identification: [List each identified cell]
Address Cell Content: [Raw text from the cell]
Multi-line Check: [Note if content spans multiple lines]
Parsed Components:
- Street Name: [Extracted street name]
- House Number: [Extracted house number]
- Postal Code: [Extracted postal code]
- City: [Extracted city]
Component Validation:
- Street Name: [Validation result]
- House Number: [Validation result]
- Postal Code: [Validation result]
- City: [Validation result]
House Number Double-Check: [Confirm house number appears twice]
Error Handling: [Describe any corrections made]
Final Address: [The final, validated address structure]
</processing>

After processing all addresses, compile them into a JSON structure as follows:

{{
"addresses": [
{{
"street_name": "string",
"house_number": "string",
"postal_code": "string",
"city": "string"
}},
// Additional addresses...
]
}}

Remember:
- All addresses should be Dutch.
- Do not include the house number in the postal_code field.
- Maintain strict adherence to the spatial order of cell contents from the image.

Now, process the addresses from the provided image(s) and present your findings in the specified format.
"""

async def process_images(images: List[UploadFile]) -> list[Address]:
    """
    Process a list of images and return the processed images as base64 strings.

    Args:
        images (List[UploadFile]): A list of image files to be processed.

    Returns:
        dict: A dictionary with base64-encoded images and OCR results.
    """
    base64_images = []
    for image in images:
        try:
            # Read the image file and encode to base64
            img_data = await image.read()
            img_base64 = base64.b64encode(img_data).decode("utf-8")
            base64_images.append(img_base64)
        except Exception as e:
            print(f"Error processing image {image.filename}: {e}")
            continue

    # Pass the base64-encoded images to the vision API or any other service
    addresses = await claude_vision_response_with_json_response(
        prompt=PROMPT, base64_images=base64_images
    )

    return [Address(**address) for address in addresses["addresses"]]
