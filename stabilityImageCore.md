## Stable Image Core API

### Description

**Stable Image Core** is the high-speed, general-purpose text-to-image generation API from Stability AI. It offers fast generation with excellent quality and requires no advanced prompt engineering.

Best for:
- Character, object, or scene prompts
- Rapid image generation at scale

---

### Usage Conditions

- **Endpoint**: `POST https://api.stability.ai/v2beta/stable-image/generate/core`
- **Authentication**: API Key in `Authorization` header (`Bearer <your-key>`)
- **Request Format**: `multipart/form-data`
- **Image Output**:
  - Default resolution: ~1.5MP (e.g., 1152x1344 or similar depending on aspect)
  - Format: `image/*` (binary) or `application/json` (base64)
- **Cost**: 3 credits per successful result

---

### Request Parameters

| Field               | Required | Type    | Description |
|--------------------|----------|---------|-------------|
| `prompt`           | ✅       | string  | Descriptive text input (max 10,000 chars) |
| `aspect_ratio`     | ❌       | enum    | One of: 16:9, 1:1 (default), 2:3, 3:2, etc. |
| `negative_prompt`  | ❌       | string  | Elements to avoid in output |
| `seed`             | ❌       | int     | 0 for random seed or fixed integer |
| `style_preset`     | ❌       | enum    | e.g. `photographic`, `anime`, `3d-model`, etc. |
| `output_format`    | ❌       | enum    | `png` (default), `jpeg`, `webp` |
| `stability-client-id`, `stability-client-user-id`, `stability-client-version` | ❌ | string | Optional metadata for debugging and moderation |

---

### Usage Example (Python)

```python
import requests

response = requests.post(
    "https://api.stability.ai/v2beta/stable-image/generate/core",
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

- A `prompt` is always required.
- `output_format` and `aspect_ratio` are optional but recommended for better control.
- You will only be charged for successful generations.

header Parameters
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

aspect_ratio	
string
Default: 1:1
Enum: 16:9 1:1 21:9 2:3 3:2 4:5 5:4 9:16 9:21
Controls the aspect ratio of the generated image.

negative_prompt	
string <= 10000 characters
A blurb of text describing what you do not wish to see in the output image. This is an advanced feature.

seed	
number [ 0 .. 4294967294 ]
Default: 0
A specific value that is used to guide the 'randomness' of the generation. (Omit this parameter or pass 0 to use a random seed.)

style_preset	
string
Enum: 3d-model analog-film anime cinematic comic-book digital-art enhance fantasy-art isometric line-art low-poly modeling-compound neon-punk origami photographic pixel-art tile-texture
Guides the image model towards a particular style.

output_format	
string
Default: png
Enum: jpeg png webp
Dictates the content-type of the generated image.

