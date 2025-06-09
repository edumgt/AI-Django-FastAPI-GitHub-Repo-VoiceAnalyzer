import torch
import numpy as np
from diffusers import TextToVideoSDPipeline
import imageio
import cv2
import os

# ✅ 프롬프트 및 환경 설정
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

# ✅ 프레임 처리 (배치 → 개별 프레임)
processed_frames = []
for i, batch in enumerate(raw_frames):
    if isinstance(batch, np.ndarray) and batch.ndim == 4:
        for j, frame in enumerate(batch):
            if frame.shape[2] in (3, 4):  # RGB or RGBA
                frame_rgb = frame[:, :, :3].astype(np.uint8)
                processed_frames.append(frame_rgb)
            else:
                print(f"⚠️ Frame {i}-{j} 채널 오류: {frame.shape}")
    else:
        print(f"⚠️ Batch {i} 형식 오류: {type(batch)}")

# ✅ 저장 (imageio 방식)
output_path_img = "output_imageio.mp4"
if processed_frames:
    with imageio.get_writer(output_path_img, fps=24, codec='libx264', quality=8) as writer:
        for frame in processed_frames:
            writer.append_data(frame)
    print(f"✅ imageio 방식 저장 완료: {output_path_img}")
else:
    print("❌ 저장할 프레임 없음.")

# ✅ 저장 (OpenCV 방식)
output_path_cv = "output_opencv.mp4"
if processed_frames:
    height, width, _ = processed_frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 또는 'avc1', 'XVID'
    out = cv2.VideoWriter(output_path_cv, fourcc, 24.0, (width, height))

    for frame in processed_frames:
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # OpenCV는 BGR 사용
        out.write(frame_bgr)

    out.release()
    print(f"✅ OpenCV 방식 저장 완료: {output_path_cv}")
else:
    print("❌ 저장할 프레임 없음.")
