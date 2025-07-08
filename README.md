# TellingMe

**나를 깨닫는 시간, 텔링미 💚**  
TellingMe는 바쁜 현대인들이 하루에 한 번, 스스로를 돌아볼 수 있도록 도와주는 감성 기반 자기 탐색 서비스입니다.  
매일 저녁 6시, 텔링미는 새로운 질문을 전송합니다. 사용자는 그날의 질문에 답하며 자신의 감정을 기록하고, 나만의 공간에서 일상의 감정을 정리할 수 있습니다.

---

## 🚀 Features

### ✅ v1 기능 (자기 탐색 및 감정 기록)

- 📮 **오늘의 질문**: 매일 18시에 새로운 질문 전송
- 🧠 **감정 분석**: 답변 기반 감정 인식 및 히스토리 확인
- 📓 **나의 공간**: 개인 답변 기록 및 정리
- 🫂 **모두의 공간**: 감정 공유를 통한 공감 커뮤니티

---

### 🆕 v2 기능 (UX 향상 및 인앱 결제 시스템)

- 🃏 **텔러카드 생성 및 꾸미기**
- 🧀 **치즈(Cheese) 결제 시스템**
- 💬 **감정 구매 기능**
- 🎯 **미션 시스템**: 일일/주간 보상 기반 서비스 이용 유도

---

## 🛠️ Tech Stack

### Language & Framework
- **Language**: Python
- **Framework**: FastAPI
- **ORM**: Tortoise ORM

### Asynchronous Task Queue
- **Task Queue**: Celery
- **Broker/Backend**: Redis

### Testing & Linting
- **Test Framework**: Pytest
- **Linting**: Ruff, Black, dmypy
- **CI Rule**: 테스트 커버리지가 90% 이상을 만족하지 않으면 병합 불가

### CI/CD
- GitHub Actions 기반
- **CI**: 커버리지 체크, 린팅, 테스트 자동 실행
- **CD**: AWS 인프라를 통한 자동 배포 (무중단 블루/그린 배포)

### Infrastructure
- **Cloud**: AWS
- **Components**:
  - Route53 (DNS)
  - Application Load Balancer
  - EC2 (배포 대상 서버)
  - RDS (Relational Database)
  - Redis (Celery 백엔드용)

---

## 🧱 Architecture

```plaintext
Client
  ↓
[ Route53 ]
  ↓
[ Load Balancer ]
  ↓                    ┌────────────┐
[ Target Group ] ───▶  │   EC2-A    │
                      │ (App v1)   │
[ Target Group ] ───▶  │   EC2-B    │
                      │ (App v2)   │
  ↓                    └────────────┘
[     RDS (MySQL)     ]
