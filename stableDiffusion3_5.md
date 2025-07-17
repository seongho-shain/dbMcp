## Stable Diffusion 3.5 API

### Description

**Stable Diffusion 3.5** is the latest generation of Stability AI's base models, offering advanced prompt adherence and image quality across multiple model sizes:

- **SD3.5 Large** (8B parameters): Professional-quality 1MP images.
- **SD3.5 Large Turbo**: Fast, 4-step image generation with near-identical quality.
- **SD3.5 Medium** (2.5B parameters): Fast, high-quality generation with optimal performance.

> All SD 3.0 API calls are automatically rerouted to SD 3.5 as of April 17, 2025.

---

### Usage Conditions

- **Endpoint**: `POST https://api.stability.ai/v2beta/stable-image/generate/sd3`
- **Authentication**: API Key in `Authorization` header (`Bearer <your-key>`)
- **Request Format**: `multipart/form-data`
- **Image Output**:
  - Default resolution: `1024x1024` (1MP)
  - Format: `image/*` or `application/json`
- **Cost**:
  - SD3.5 Large: 6.5 credits
  - SD3.5 Large Turbo: 4 credits
  - SD3.5 Medium: 3.5 credits

---

### Request Parameters

| Field            | Required | Type     | Description |
|------------------|----------|----------|-------------|
| `prompt`         | ✅        | string   | Description of desired image (max 10,000 chars) |
| `mode`           | ❌        | enum     | `text-to-image` (default) or `image-to-image` |
| `image`          | ❌        | binary   | Input image (required for `image-to-image`) |
| `strength`       | ❌        | float    | Degree of transformation (required for `image-to-image`) |
| `aspect_ratio`   | ❌        | enum     | One of: 1:1 (default), 16:9, 3:2, etc. Only for `text-to-image` |
| `model`          | ❌        | enum     | `sd3.5-large` (default), `sd3.5-large-turbo`, `sd3.5-medium` |
| `output_format`  | ❌        | enum     | `png` (default), `jpeg` |
| `seed`           | ❌        | int      | Fixed or random generation seed |
| `cfg_scale`      | ❌        | float    | Adherence to prompt (1–10). Default: 4 (Large/Medium), 1 (Turbo) |
| `negative_prompt`| ❌        | string   | Elements to exclude from output |
| `style_preset`   | ❌        | enum     | e.g. `anime`, `photographic`, `pixel-art`, etc. |

---

### Usage Example (Python)

```python
import requests

response = requests.post(
    "https://api.stability.ai/v2beta/stable-image/generate/sd3",
    headers={
        "authorization": "Bearer sk-MYAPIKEY",
        "accept": "image/*"
    },
    files={"none": ''},
    data={
        "prompt": "Lighthouse on a cliff overlooking the ocean",
        "output_format": "jpeg",
    },
)

if response.status_code == 200:
    with open("./lighthouse.jpeg", 'wb') as file:
        file.write(response.content)
else:
    raise Exception(response.json())
```

---

### Warnings

- `image`, `strength`, and `mode=image-to-image` are required together.
- `aspect_ratio` is only valid for `text-to-image` mode.
- Total request size must be ≤ 10MiB.
- All model variants generate 1MP images regardless of aspect ratio.

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

mode	
string (GenerationMode)
Default: text-to-image
Enum: image-to-image text-to-image
Controls whether this is a text-to-image or image-to-image generation, which affects which parameters are required:

text-to-image requires only the prompt parameter
image-to-image requires the prompt, image, and strength parameters
image	
string <binary>
The image to use as the starting point for the generation.

Supported formats:

jpeg
png
webp
Supported dimensions:

Every side must be at least 64 pixels
Important: This parameter is only valid for image-to-image requests.

strength	
number [ 0 .. 1 ]
Sometimes referred to as denoising, this parameter controls how much influence the image parameter has on the generated image. A value of 0 would yield an image that is identical to the input. A value of 1 would be as if you passed in no image at all.

Important: This parameter is only valid for image-to-image requests.

aspect_ratio	
string
Default: 1:1
Enum: 16:9 1:1 21:9 2:3 3:2 4:5 5:4 9:16 9:21
Controls the aspect ratio of the generated image. Defaults to 1:1.

Important: This parameter is only valid for text-to-image requests.

model	
string
Default: sd3.5-large
Enum: sd3.5-large sd3.5-large-turbo sd3.5-medium
The model to use for generation.

sd3.5-large requires 6.5 credits per generation
sd3.5-large-turbo requires 4 credits per generation
sd3.5-medium requires 3.5 credits per generation
As of the April 17, 2025, sd3-large, sd3-large-turbo and sd3-medium are re-routed to their sd3.5-[model version] equivalent, at the same price.
seed	
number [ 0 .. 4294967294 ]
Default: 0
A specific value that is used to guide the 'randomness' of the generation. (Omit this parameter or pass 0 to use a random seed.)

output_format	
string
Default: png
Enum: jpeg png
Dictates the content-type of the generated image.

style_preset	
string
Enum: 3d-model analog-film anime cinematic comic-book digital-art enhance fantasy-art isometric line-art low-poly modeling-compound neon-punk origami photographic pixel-art tile-texture
Guides the image model towards a particular style.

negative_prompt	
string <= 10000 characters
Keywords of what you do not wish to see in the output image. This is an advanced feature.

cfg_scale	
number [ 1 .. 10 ]
How strictly the diffusion process adheres to the prompt text (higher values keep your image closer to your prompt). The Large and Medium models use a default of 4. The Turbo model uses a default of 1.