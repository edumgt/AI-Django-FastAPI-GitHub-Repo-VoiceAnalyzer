import os
import random
from google.cloud import texttospeech

# 서비스 계정 JSON 파일 경로 (여기에 본인 경로 입력)
SERVICE_ACCOUNT_FILE = "my-project.json"

# Google TTS 클라이언트 생성
client = texttospeech.TextToSpeechClient.from_service_account_file(SERVICE_ACCOUNT_FILE)

# 사용할 목소리 후보 리스트
voice_names = ["ko-KR-Wavenet-A", "ko-KR-Wavenet-B", "ko-KR-Wavenet-C", "ko-KR-Wavenet-D"]

# 랜덤으로 하나 선택
selected_voice = random.choice(voice_names)
print(f"🎙️ 선택된 목소리: {selected_voice}")

# TTS 입력 텍스트
synthesis_input = texttospeech.SynthesisInput(
    text=""""""
)

# 목소리 설정
voice = texttospeech.VoiceSelectionParams(
    language_code="ko-KR",
    name=selected_voice,
    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
)

# 오디오 설정 (속도 1.1배)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3,
    speaking_rate=1.1
)


base_filename = "Java_Example"
extension = ".mp3"
counter = 1

# 현재 디렉토리에서 가장 큰 번호 찾기
while os.path.exists(f"{base_filename}{counter}{extension}"):
    counter += 1

output_file = f"{base_filename}{counter}{extension}"

# TTS API 호출
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# MP3로 저장
with open(output_file, "wb") as out:
    out.write(response.audio_content)
    print(f"✅ Google TTS 한글 mp3 파일 생성 완료: {output_file}")
