# STRIKERS 2022

> Pygame 기반 2인 협동 슈팅 게임을 클린 아키텍처로 재구성한 프로젝트

## 프로젝트 소개

STRIKERS 2022는 Pygame으로 개발한 2인용 슈팅 게임이다. 두 명의 플레이어가 협동하여 적들을 물리치고 보스를 처치하는 것이 목표이다.

1학년 때 작성한 단일 파일 코드를 **관심사 분리(Separation of Concerns)** 원칙에 따라 모듈화하고, 성능 최적화 및 크로스 플랫폼 지원을 추가했다.

### 게임 특징

- 2인 협동 플레이
- 적 처치 시 아이템 드롭
- 무기 업그레이드 시스템 (공격력, 공격속도, 무기 개수)
- 보스전

---

## 기존 코드의 문제점

리팩토링 전 코드는 4개의 파일로 구성되어 있었다. (`git show eb1533d`로 확인 가능)

```
STRIKERS 2022.py  (516줄) - 게임 루프, 메뉴, 모든 게임 로직
defmd.py          (75줄)  - 유틸리티 함수, Item 클래스
plymd.py          (67줄)  - Player, Player_Weapon 클래스
enemd.py          (121줄) - Boss, Enemy, Enemy_Weapon 클래스
```

### 1. God Function

`game_loop()` 함수 하나에 450줄 이상의 코드가 집중되어 있었다. 입력 처리, 공격 로직, 적 생성, 충돌 처리, 렌더링, 게임 오버 판정까지 모든 것이 한 함수에 있어 가독성과 유지보수성이 떨어졌다.

### 2. 매직 넘버

`26`, `3`, `100`, `5000` 등의 숫자가 코드 전반에 하드코딩되어 있어 의미 파악이 어려웠다. 예를 들어 `26 - player1_weapon_speed_level * 3`이라는 표현에서 26과 3이 무엇을 의미하는지 코드만으로는 알 수 없었다.

### 3. 코드 중복

Player 1과 Player 2의 입력 처리, 공격 로직, 충돌 처리가 거의 동일한 코드로 두 번씩 작성되어 있었다. 변경 사항이 생기면 두 곳을 모두 수정해야 했다.

### 4. 전역 상태

플레이어 상태가 `player1_attack_go1`, `player1_weapon_speed_level` 등 14개의 개별 변수로 흩어져 있어 관련 데이터를 한눈에 파악하기 어려웠다.

### 5. 플랫폼 의존성

`C:/Windows/Fonts/ariblk.ttf`처럼 Windows 전용 경로가 하드코딩되어 macOS나 Linux에서 실행할 수 없었다.

### 6. 성능 문제

충돌 발생 시마다 `pygame.display.update()`를 호출하고, 엔티티 생성 시마다 이미지를 새로 로드하여 불필요한 오버헤드가 발생했다.

---

## 리팩토링

### 1. 상수 분리

매직 넘버를 `config/settings.py`에 명명된 상수로 분리했다. `ATTACK_COOLDOWN_BASE = 26`처럼 이름을 붙이면 코드가 곧 문서가 된다.

### 2. 상태 캡슐화

흩어진 플레이어 변수들을 `PlayerState` 클래스로 묶었다. 관련 데이터와 로직(공격 가능 여부 판정, 레벨업 등)이 한 곳에 모여 응집도가 높아졌다.

### 3. 중복 제거

두 플레이어의 공통 로직을 메서드로 추출하여 `_handle_player_attack(player, weapons)` 형태로 재사용한다.

### 4. 책임 분리 (Manager 패턴)

450줄의 단일 함수를 `InputManager`, `CollisionManager`, `SpawnManager`, `AudioManager`로 분리했다. 각 매니저는 하나의 책임만 가진다.

### 5. 크로스 플랫폼 지원

`FontManager`가 OS별로 사용 가능한 폰트를 자동 탐지한다.

### 6. 성능 최적화

- 화면 갱신: 충돌 시마다가 아닌, 프레임당 한 번만 `pygame.display.flip()` 호출
- 이미지 캐싱: 클래스 레벨 `_image_cache`로 동일 이미지 중복 로드 방지

### 결과

| 구분 | Before | After |
|------|--------|-------|
| 파일 수 | 4개 | 21개 |
| 평균 파일 크기 | ~195줄 | ~57줄 |
| 최대 함수 길이 | 450줄 | ~50줄 |

총 라인 수는 증가했지만, 각 파일과 함수가 **단일 책임**을 가지게 되어 유지보수성이 향상되었다.

---

## 아키텍처

### 디렉토리 구조

```
strikers2022/
├── __init__.py              # 패키지 진입점
├── __main__.py              # python -m 지원
├── main.py                  # 메인 함수
├── game.py                  # Game 클래스 (메인 루프)
├── config/
│   ├── settings.py          # 게임 상수 (WINDOW_WIDTH, FPS 등)
│   └── assets.py            # 리소스 경로 관리
├── entities/
│   ├── base.py              # GameEntity 추상 클래스
│   ├── player.py            # Player, PlayerState
│   ├── weapon.py            # PlayerWeapon, EnemyWeapon
│   ├── enemy.py             # Enemy
│   ├── boss.py              # Boss
│   └── item.py              # Item, ItemType
├── managers/
│   ├── input_manager.py     # 입력 처리
│   ├── collision_manager.py # 충돌 처리
│   ├── spawn_manager.py     # 스폰 관리
│   └── audio_manager.py     # 오디오 관리
├── ui/
│   ├── fonts.py             # 크로스 플랫폼 폰트
│   ├── hud.py               # HUD (체력, 점수 등)
│   └── menu.py              # 게임 메뉴
└── utils/
    └── math_utils.py        # 수학 유틸리티
```

### 클래스 다이어그램

```
pygame.sprite.Sprite
        │
        ▼
   GameEntity (ABC)
   ├── crash()
   └── draw()
        │
        ├── Player ──── PlayerState
        │                 ├── weapon_speed_level
        │                 ├── weapon_power_level
        │                 ├── weapon_number_level
        │                 └── can_attack(), upgrade_*()
        │
        ├── Enemy
        ├── Boss
        ├── PlayerWeapon
        ├── EnemyWeapon
        └── Item ──── ItemType (Enum)
```

---

## 주요 설계 결정

### 1. 상태 캡슐화 (PlayerState)

플레이어 관련 변수들을 `PlayerState` 클래스로 묶어 관리한다.

```python
class PlayerState:
    def __init__(self):
        self.weapon_speed_level = 1
        self.weapon_power_level = 1
        self.weapon_number_level = 1
        self.attack_go1 = False
        self.attack_go2 = False
        self.attack_counter = 0

    def can_attack(self) -> bool:
        return (self.attack_go1
                and self.attack_counter % self.attack_delay == 0
                and self.attack_go2)
```

### 2. 매니저 패턴

게임 로직을 역할별로 분리한다.

| 매니저 | 역할 |
|--------|------|
| `InputManager` | 키 입력 처리, 플레이어 이동/공격 |
| `CollisionManager` | 모든 충돌 감지 및 처리 |
| `SpawnManager` | 적/아이템 스폰 로직 |
| `AudioManager` | 사운드/BGM 재생 |

### 3. 이미지 캐싱

엔티티 생성 시마다 이미지를 로드하는 대신, 클래스 레벨 캐시를 사용한다.

```python
class PlayerWeapon(GameEntity):
    _image_cache: dict[int, tuple[Surface, Mask]] = {}

    def __init__(self, ...):
        if power_level not in cls._image_cache:
            img = pygame.image.load(...).convert_alpha()
            cls._image_cache[power_level] = (img, pygame.mask.from_surface(img))
        self.image, self.mask = cls._image_cache[power_level]
```

### 4. 크로스 플랫폼 폰트

Windows, macOS, Linux 모두에서 실행 가능하도록 시스템 폰트를 자동 탐지한다.

```python
font_options = {
    "Windows": ["C:/Windows/Fonts/ariblk.ttf", ...],
    "Darwin": ["/System/Library/Fonts/Helvetica.ttc", ...],
    "Linux": ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", ...],
}
```

---

## 게임 에셋

모든 에셋(이미지, 사운드, BGM)은 외부 라이브러리 없이 **순수 Python**만으로 생성했다.

---

## 실행 방법

### 요구사항

- Python 3.12+
- pygame 2.6.1

### 설치

```bash
pip install -r requirements.txt
```

### 실행

```bash
python run_game.py
# 또는
python -m strikers2022
```

### 조작법

| Player | 이동 | 공격 |
|--------|------|------|
| Player 1 | 방향키 (↑↓←→) | Numpad 0 |
| Player 2 | WASD | Space |

---

## 주요 상수 (config/settings.py)

| 상수 | 값 | 설명 |
|------|-----|------|
| `WINDOW_WIDTH/HEIGHT` | 1000 | 화면 크기 |
| `FPS` | 60 | 프레임 레이트 |
| `PLAYER_HP` | 1000 | 공유 체력 |
| `BOSS_DEFAULT_HP` | 5000 | 보스 체력 |
| `ATTACK_COOLDOWN_BASE` | 26 | 공격 쿨다운 기본값 |
| `MAX_WEAPON_*_LEVEL` | 4~5 | 무기 레벨 상한 |

---

## 향후 개선 가능 사항

- [ ] 설정 파일 (JSON/YAML) 외부화
- [ ] 게임 저장/불러오기 기능
- [ ] 유닛 테스트 추가
- [ ] 스프라이트 시트 사용으로 성능 최적화