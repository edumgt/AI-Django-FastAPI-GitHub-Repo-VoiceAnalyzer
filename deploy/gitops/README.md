# GitOps Environment Profiles

이 디렉터리는 배포 목표 상태를 Git으로 관리하기 위한 GitOps 선언 파일입니다.

- `environments/dev.json`: `develop` 배포 대상
- `environments/prod.json`: `main` 배포 대상
- `environments/local.json`: 수동 실행 검증 대상

각 파일의 핵심 필드:
- `environment`: 환경명 (`local`/`dev`/`prod`)
- `branch`: 이 환경이 허용하는 Git 브랜치
- `aws_region`: 대상 AWS 리전
- `codepipeline_name`: 실행할 CodePipeline 이름
- `wait_for_completion`: 파이프라인 완료 대기 여부

변경 원칙:
1. 환경 파일 수정 -> Pull Request 생성
2. 리뷰/승인 후 머지
3. GitHub Actions가 변경된 목표 상태를 읽어 CodePipeline 실행
