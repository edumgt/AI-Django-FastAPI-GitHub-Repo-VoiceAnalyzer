from diffusers import DiffusionPipeline
import torch
import imageio

pipe = DiffusionPipeline.from_pretrained(
    "damo-vilab/text-to-video-ms-1.7b",
    torch_dtype=torch.float16,
    variant="fp16"
).to("cuda")

prompt = "A panda playing guitar in the forest"
output = pipe(prompt, num_inference_steps=25, num_frames=16)

frames = getattr(output, "frames", None)
if frames is None or len(frames) == 0:
    print("❌ No valid frames generated.")
    exit()

imageio.mimsave("output.mp4", frames, fps=8)
print("✅ Video saved as output.mp4")
