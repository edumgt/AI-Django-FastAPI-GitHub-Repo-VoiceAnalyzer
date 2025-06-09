import torch
from diffusers import TextToVideoSDPipeline
import imageio
import os

# 1. 디바이스 선택 (CUDA 멀티 GPU)
device = "cuda" if torch.cuda.is_available() else "cpu"
gpu_count = torch.cuda.device_count()
target_device = torch.device("cuda:0" if gpu_count > 0 else "cpu")

print(f"🖥 사용 가능한 GPU 개수: {gpu_count}")
print(f"📌 사용 디바이스: {target_device}")

# 2. 파이프라인 로드 (ZeroScope XL)
model_id = "cerspense/zeroscope_v2_XL"

pipe = TextToVideoSDPipeline.from_pretrained(
    "Ali-VILab/text-to-video-ms-1.7b",  # 예시
    torch_dtype=torch.float16,
    use_safetensors=True
).to("cuda")


# 3. 최적화 옵션
pipe.enable_attention_slicing()
pipe.enable_model_cpu_offload()  # CPU로 일부 레이어 이동
pipe.enable_vae_slicing()

# 4. 프롬프트 설정
prompt = "A serene landscape with mountains and a lake, sunset lighting, cinematic tone"

# 5. 생성 실행
output = pipe(
    prompt,
    num_inference_steps=25,
    guidance_scale=7.5,
)

# 6. 프레임 저장
video_frames = output.frames
output_path = "zeroscope_output.mp4"
imageio.mimsave(output_path, video_frames, fps=24)
print(f"✅ 저장 완료: {output_path}")
