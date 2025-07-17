## Stable Image Ultra API

### Description

**Stable Image Ultra** is Stability AI's most advanced text-to-image generation service, built on top of Stable Diffusion 3.5. It delivers exceptional image quality, especially in areas like:
- Typography
- Dynamic lighting
- Color vibrancy
- Complex composition

The service accepts text prompts and optionally reference images, returning 1-megapixel images by default.

---

### Usage Conditions

- **Endpoint**: `POST https://api.stability.ai/v2beta/stable-image/generate/ultra`
- **Authentication**: API Key in `Authorization` header (`Bearer <your-key>`)
- **Request Format**: `multipart/form-data`
- **Image Output**:
  - Default: `1024x1024` resolution
  - Format: `image/*` (raw image) or `application/json` (base64-encoded image)
- **Cost**: 8 credits per successful result (free if failed)

---

### Request Parameters

| Field               | Required | Type    | Description |
|--------------------|----------|---------|-------------|
| `prompt`           | ✅       | string  | Main text input (max 10,000 chars) |
| `image`            | ❌       | binary  | Optional reference image (required if `strength` is used) |
| `strength`         | ❌       | float   | 0.0–1.0 control of image influence |
| `negative_prompt`  | ❌       | string  | Things to avoid in output |
| `aspect_ratio`     | ❌       | enum    | One of: 16:9, 1:1 (default), 2:3, 3:2, etc. |
| `seed`             | ❌       | int     | Random seed (0 = random) |
| `output_format`    | ❌       | enum    | `png` (default), `jpeg`, `webp` |
| `style_preset`     | ❌       | enum    | e.g. `photographic`, `anime`, `3d-model`, etc. |
| `stability-client-id`, `stability-client-user-id`, `stability-client-version` | ❌ | string | Optional for debugging/analytics |

---

### Usage Example (Python)

```python
import requests

response = requests.post(
    "https://api.stability.ai/v2beta/stable-image/generate/ultra",
    headers={
        "authorization": "Bearer sk-MYAPIKEY",
        "accept": "image/*"
    },
    files={"none": ''},
    data={
        "prompt": "Lighthouse on a cliff overlooking the ocean",
        "output_format": "webp",
    },
)

if response.status_code == 200:
    with open("./lighthouse.webp", 'wb') as file:
        file.write(response.content)
else:
    raise Exception(response.json())
```

---

### Warnings

- You **must** provide the `strength` parameter if using an input `image`.
- Output is **always** 1MP regardless of aspect ratio.
- For exact parameter behavior, refer to official request schema.
- Overuse of vague prompts (e.g. "beautiful scene") may reduce output quality.


authorization
required
string non-empty
Your Stability API key, used to authenticate your requests. Although you may have multiple keys in your account, you should use the same key for all requests to this API.

content-type
required
string non-empty
Example: multipart/form-data
The content type of the request body. Do not manually specify this header; your HTTP client library will automatically include the appropriate boundary parameter.

accept	
string
Default: image/*
Enum: application/json image/*
Specify image/* to receive the bytes of the image directly. Otherwise specify application/json to receive the image as base64 encoded JSON.

stability-client-id	
string (StabilityClientID) <= 256 characters
Example: my-awesome-app
The name of your application, used to help us communicate app-specific debugging or moderation issues to you.

stability-client-user-id	
string (StabilityClientUserID) <= 256 characters
Example: DiscordUser#9999
A unique identifier for your end user. Used to help us communicate user-specific debugging or moderation issues to you. Feel free to obfuscate this value to protect user privacy.

stability-client-version	
string (StabilityClientVersion) <= 256 characters
Example: 1.2.1
The version of your application, used to help us communicate version-specific debugging or moderation issues to you.

Request Body schema: multipart/form-data
prompt
required
string [ 1 .. 10000 ] characters
What you wish to see in the output image. A strong, descriptive prompt that clearly defines elements, colors, and subjects will lead to better results.

To control the weight of a given word use the format (word:weight), where word is the word you'd like to control the weight of and weight is a value between 0 and 1. For example: The sky was a crisp (blue:0.3) and (green:0.8) would convey a sky that was blue and green, but more green than blue.

negative_prompt	
string <= 10000 characters
A blurb of text describing what you do not wish to see in the output image. This is an advanced feature.

aspect_ratio	
string
Default: 1:1
Enum: 16:9 1:1 21:9 2:3 3:2 4:5 5:4 9:16 9:21
Controls the aspect ratio of the generated image.

seed	
number [ 0 .. 4294967294 ]
Default: 0
A specific value that is used to guide the 'randomness' of the generation. (Omit this parameter or pass 0 to use a random seed.)

output_format	
string
Default: png
Enum: jpeg png webp
Dictates the content-type of the generated image.

image	
string <binary>
The image to use as the starting point for the generation.

Important: The strength parameter is required when image is provided.

Supported Formats:

jpeg
png
webp
Validation Rules:

Width must be between 64 and 16,384 pixels
Height must be between 64 and 16,384 pixels
Total pixel count must be at least 4,096 pixels
style_preset	
string
Enum: 3d-model analog-film anime cinematic comic-book digital-art enhance fantasy-art isometric line-art low-poly modeling-compound neon-punk origami photographic pixel-art tile-texture
Guides the image model towards a particular style.

strength	
number [ 0 .. 1 ]
Sometimes referred to as denoising, this parameter controls how much influence the image parameter has on the generated image. A value of 0 would yield an image that is identical to the input. A value of 1 would be as if you passed in no image at all.

Important: This parameter is required when image is provided.