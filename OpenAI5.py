import torch
import numpy as np
from diffusers import TextToVideoSDPipeline
import imageio
import os

# ✅ 환경 설정
prompt = "A magical forest with glowing plants and fireflies at night"
device = "cuda" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if device == "cuda" else torch.float32

# ✅ 파이프라인 로딩
pipe = TextToVideoSDPipeline.from_pretrained(
    "Ali-VILab/text-to-video-ms-1.7b",
    torch_dtype=torch_dtype,
    use_safetensors=True
).to(device)

pipe.enable_attention_slicing()
pipe.enable_vae_slicing()
pipe.enable_model_cpu_offload()

# ✅ 비디오 생성
output = pipe(prompt, num_inference_steps=25, guidance_scale=7.5)

# ✅ 프레임 추출
if hasattr(output, "frames"):
    raw_frames = output.frames
elif isinstance(output, dict) and "frames" in output:
    raw_frames = output["frames"]
else:
    raise ValueError("출력에서 frames를 찾을 수 없습니다.")

# ✅ 영상 데이터 분해 및 처리
processed_frames = []
for i, batch in enumerate(raw_frames):
    if isinstance(batch, np.ndarray) and batch.ndim == 4:
        for j, frame in enumerate(batch):
            if frame.shape[2] in (3, 4):
                processed_frames.append(frame.astype(np.uint8))
            else:
                print(f"⚠️ Frame {i}-{j} 채널 이상: {frame.shape}")
    else:
        print(f"⚠️ Batch {i} 형식 이상: {type(batch)}, ndim={getattr(batch, 'ndim', 'N/A')}")

# ✅ 저장
output_path = "output.mp4"
if processed_frames:
    with imageio.get_writer(output_path, fps=24, codec='libx264', quality=8) as writer:
        for frame in processed_frames:
            writer.append_data(frame)
    print(f"✅ MP4 저장 완료: {output_path}")
else:
    print("❌ 저장할 프레임 없음.")
