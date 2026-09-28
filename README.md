```markdown
# ROS 2 Turtle Control

ROS 2와 PyQt5를 이용한 TurtleSim 제어 GUI 프로젝트입니다.

방향 버튼으로 Turtle을 제어하고, 현재 위치를 실시간으로 확인할 수 있습니다.  
`SAVE` 버튼을 누르면 현재 Turtle의 위치 정보가 MySQL 데이터베이스에 저장됩니다.

---

## 1. 프로젝트 구성

```text
ros-turtle-control/
├── README.md
├── src/
│   └── turtle_control/
│       ├── turtle_control/
│       │   └── turtle_controller.py
│       ├── package.xml
│       ├── setup.py
│       └── ...
├── pyqt/
│   └── turtle_gui.py
├── mysql/
│   └── create_rosdb.sql
└── .gitignore

```

---

## 2. 주요 기능

### Turtle 제어

PyQt5 GUI의 버튼을 이용하여 TurtleSim의 `turtle1`을 제어합니다.

| 버튼 | 기능 |
| --- | --- |
| **↑** | 전진 |
| **↓** | 후진 |
| **←** | 좌회전 |
| **→** | 우회전 |
| **RESET** | Turtle 위치 초기화 |
| **SAVE** | 현재 위치를 MySQL에 저장 |

GUI에서 입력한 명령은 `/turtle_command` 토픽을 통해 `turtle_controller` 노드로 전달됩니다.

```text
[PyQt GUI]
    │
    │ /turtle_command
    ▼
[turtle_controller]
    │
    │ /turtle1/cmd_vel
    ▼
[turtlesim_node]

```

---

## 3. 자체 개발 기능

기본 Turtle 제어 기능에 더해 다음 기능을 구현했습니다.

### 실시간 위치 표시

TurtleSim의 `/turtle1/pose` 토픽을 구독하여 현재 Turtle의 위치와 방향을 GUI에 실시간으로 표시합니다.

* `X`: X 좌표
* `Y`: Y 좌표
* `θ`: 방향 (Orientation)

### GUI 개선

기존 GUI의 기본 배치를 수정하여 다음과 같이 개선했습니다.

* GUI 크기 및 버튼 배치 최적화
* 방향 버튼 스타일 변경
* `RESET` / `SAVE` 버튼 스타일 시각적 구분
* 현재 위치 정보 표시 영역 추가
* 버튼 Hover / Press 효과 추가

---

## 4. MySQL 저장 기능

`SAVE` 버튼을 누르면 현재 Turtle의 위치 정보가 MySQL 데이터베이스에 저장됩니다.

### 데이터베이스 구조

* **Database**: `rosdb`
* **Table**: `turtlepos`

| 컬럼 | 타입 | 설명 |
| --- | --- | --- |
| `id` | `INT` | 자동 증가 기본키 (AUTO_INCREMENT PRIMARY KEY) |
| `x` | `FLOAT` | Turtle X 좌표 |
| `y` | `FLOAT` | Turtle Y 좌표 |
| `theta` | `FLOAT` | Turtle 방향 |
| `time` | `DATETIME` | 데이터 저장 시간 |

---

## 5. 실행 환경

* **OS**: Ubuntu 22.04 LTS
* **ROS**: ROS 2 Humble
* **Language**: Python 3
* **GUI**: PyQt5
* **Database**: MySQL 8.0
* **Simulator**: turtlesim

---

## 6. ROS 2 패키지 빌드

```bash
cd ~/ros-turtle-control
colcon build --packages-select turtle_control
source install/setup.bash

```

패키지 설치 여부를 확인합니다.

```bash
ros2 pkg list | grep turtle_control

```

---

## 7. MySQL 설정

프로젝트에 포함된 SQL 파일을 이용하여 데이터베이스와 테이블을 생성합니다.

```bash
mysql -u root -p < mysql/create_rosdb.sql

```

Python 프로그램에서 사용할 MySQL 계정을 생성하고 권한을 부여합니다.

```sql
CREATE USER 'rosuser'@'localhost' IDENTIFIED BY '사용할_비밀번호';
GRANT ALL PRIVILEGES ON rosdb.* TO 'rosuser'@'localhost';
FLUSH PRIVILEGES;

```

---

## 8. 데이터베이스 비밀번호 설정

데이터베이스 비밀번호는 소스 코드에 하드코딩하지 않고 환경변수로 관리합니다.

```bash
export ROS_DB_PASSWORD='사용할_비밀번호'

```

---

## 9. 실행 방법

### 1. TurtleSim 실행

첫 번째 터미널에서 실행합니다.

```bash
source /opt/ros/humble/setup.bash
ros2 run turtlesim turtlesim_node

```

### 2. Turtle Controller 실행

두 번째 터미널에서 실행합니다.

```bash
cd ~/ros-turtle-control
source install/setup.bash
ros2 run turtle_control turtle_controller

```

### 3. PyQt GUI 실행

세 번째 터미널에서 실행합니다.

```bash
cd ~/ros-turtle-control
export ROS_DB_PASSWORD='사용할_비밀번호'
python3 pyqt/turtle_gui.py

```

---

## 10. GUI 구성 및 사용법

GUI는 다음 6개의 기본 버튼으로 구성됩니다.

* **방향키 (`↑`, `↓`, `←`, `→`)**: Turtle을 이동시키며, 이동에 따라 GUI 하단에 현재 `X`, `Y`, `θ` 값이 실시간으로 업데이트됩니다.
* **RESET**: Turtle의 위치를 초기 상태로 리셋합니다.
* **SAVE**: 현재 위치 데이터와 기록 시간을 MySQL의 `turtlepos` 테이블에 저장합니다.

---

## 11. 프로젝트 특징

* 직접 제작한 ROS 2 Python 패키지 기반 동작
* ROS 2 Publisher / Subscriber 아키텍처 적용
* PyQt5를 활용한 사용자 친화적 GUI 구현
* Turtle Pose 실시간 인터랙션 및 표시
* MySQL 연동을 통한 데이터 영속성 확보
* 환경변수를 활용한 DB 보안 관리

```

```
