import torch
import numpy as np
from diffusers import TextToVideoSDPipeline
from PIL import Image
import imageio
import os

# ✅ 설정
prompt = "A magical forest with glowing plants and fireflies at night"
device = "cuda" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if device == "cuda" else torch.float32

# ✅ 모델 로딩
pipe = TextToVideoSDPipeline.from_pretrained(
    "Ali-VILab/text-to-video-ms-1.7b",
    torch_dtype=torch_dtype,
    use_safetensors=True
).to(device)

pipe.enable_attention_slicing()
pipe.enable_vae_slicing()
pipe.enable_model_cpu_offload()

# ✅ 프롬프트 기반 비디오 생성
output = pipe(prompt, num_inference_steps=25, guidance_scale=7.5)

# ✅ 프레임 추출
if hasattr(output, "frames"):
    video_frames = output.frames
elif isinstance(output, dict) and "frames" in output:
    video_frames = output["frames"]
else:
    raise ValueError("출력에 'frames'가 없습니다.")

# ✅ 이미지 RGB 변환 및 numpy 변환
processed_frames = []
for i, frame in enumerate(video_frames):
    try:
        if isinstance(frame, Image.Image):
            rgb = frame.convert("RGB")
            arr = np.array(rgb)
            if arr.ndim == 3 and arr.shape[2] == 3:
                processed_frames.append(arr)
            else:
                print(f"⚠️ Frame {i} is not RGB: {arr.shape}")
        else:
            print(f"⚠️ Frame {i} is not Image.Image: {type(frame)}")
    except Exception as e:
        print(f"❌ Frame {i} error: {e}")

# ✅ MP4 비디오로 저장
output_path = "output.mp4"
fps = 24

if processed_frames:
    writer = imageio.get_writer(output_path, fps=fps, codec='libx264', quality=8)
    for frame in processed_frames:
        writer.append_data(frame)
    writer.close()
    print(f"✅ Saved video to {output_path}")
else:
    print("❌ No valid frames to write.")
