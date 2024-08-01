## Для пользователя
Калькулятор сделан для вычисления арифметических выражений. Запуск производится из командной строки.

**Основные функции калькулятора:**
- Поддержка инфиксной записи
- Поддержка постфиксной записи
- Поддержка операций со скобками
- Поддержка приоритезации операций в выражении

**Поддерживаемые среды:**
- Linux (Debian/Ubuntu)
- Windows

**Минимальные требования:**

*Для Linux:*
- Интерпретатор C++ (gcc / g++ -std=c++17)
- Cmake

*Для Windows:*
- Наличие git / cmd
- Cmake
- Chocolatey
- Mingw64

**Руководство по использованию:**
Запуск производится из командной строки. Выполняет основные арифметические операции. Возможны 2 формы записи:
- **Инфиксная** (знак операции ставится между операндами: `3+5`)
- **Постфиксная** (знак операции ставится после операндов: `3 5 +`)

Возможно использование скобок для приоритизации конкретных действий в выражении.

**Примеры использования:**
- `(3 + 5) / 6 * 3`
- `7 / (6 - 2) * 8 - (3 - 5)`
- `3 5 8 * +`
- `3 5 6 3 + / *`

## Для разработчика

### 1. Состав проекта
```
lab-repository/
├── docs/
│   └── .gitkeep
├── lint/
│   ├── .gitkeep
│   ├── lint_code_syntax.py
│   └── lint_copyright.py
├── scr/
│   ├── .gitkeep
│   ├── infix_calculator.cpp
│   ├── infix_calculator.h
│   ├── infix_calculator_gui.cpp
│   ├── infix_calculator_gui.h
│   ├── linked_list.h
│   ├── main.cpp
│   ├── postfix_calculator.cpp
│   ├── postfix_calculator.h
│   ├── queue.h
│   └── stack.h
├── tests/
│   ├── .gitkeep
│   ├── test_calculator.cpp
│   └── test_use_case.cpp
├── .gitlab-ci.yml
├── CMakeLists.txt
├── Dockerfile
├── LICENSE
└── README.md
```

### 2. Поддерживаемые среды
- Windows
- Linux (Ubuntu/Debian)

### 3. Используемые библиотеки
**C++:**
- `<iostream>`
- `<gtest>`
- `<utility>`
- `<cstdint>`
- `<string>`

**Python:**
- `<os>`
- `<subprocess>`

### 4. Требования к окружению разработки

*Для Windows:*
- Python 3
- CMake
- Git/cmd
- GitLab-Runner
- Mingw64
- Chocolatey
- Cppcheck

*Для Linux:*
- G++ компилятор
- Cpack
- Cmake
- Ctest
- apk
- Git
- DockerCE
- Python
- system cmd

### 5. CI/CD
Настройка CI/CD в GitLab:

**Описание `.gitlab-ci.yml`**

```yaml
stages:
  - linter
  - build
  - test
  - deploy
  - package

linter_1:
  stage: linter
  script: 
    - python3 lint/lint_copyright.py
  tags:
    - lint

linter_2:
  stage: linter
  script: 
    - python3 lint/lint_code_syntax.py
  tags:
    - lint

build_ubuntu:
  stage: build
  script:
    - g++ -std=c++17 scr/main.cpp scr/infix_calculator_gui.cpp scr/infix_calculator_gui.h scr/infix_calculator.cpp scr/infix_calculator.h scr/postfix_calculator.cpp scr/postfix_calculator.h scr/queue.h scr/stack.h scr/linked_list.h 
  tags:
    - ubuntu

build_debian:
  stage: build
  script:
    - g++ -std=c++17 scr/main.cpp scr/infix_calculator_gui.cpp scr/infix_calculator_gui.h scr/infix_calculator.cpp scr/infix_calculator.h scr/postfix_calculator.cpp scr/postfix_calculator.h scr/queue.h scr/stack.h scr/linked_list.h 
  tags:
    - debian

build_win:
  stage: build
  tags:
    - windows
  script:
    - g++ -std=c++17 scr/main.cpp scr/infix_calculator_gui.cpp scr/infix_calculator_gui.h scr/infix_calculator.cpp scr/infix_calculator.h scr/postfix_calculator.cpp scr/postfix_calculator.h scr/queue.h scr/stack.h scr/linked_list.h 

build_docker:
  stage: build
  script:
    - docker build -t myapp .
  tags:
    - ubuntu

unit_tests:
  stage: test
  script:
    - cmake .  
    - make
    - ctest --output-on-failure  
  tags:
    - test1

use_case_tests:
  stage: test
  script:
    - cmake . 
    - make  
    - ctest --output-on-failure  
  tags:
    - test2

deploy:
  stage: deploy
  script:
    - echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
    - docker tag myapp $DOCKER_USERNAME/myapp:latest
    - docker push $DOCKER_USERNAME/myapp:latest
  only:
    - deploydocker
  tags:
    - deploy

package_ubuntu:
  stage: package
  image: alpine:latest
  dependencies:
    - build_ubuntu
  script:
    - mkdir build
    - cd build
    - cmake .. 
    - cmake --build . --target package
    - zip -r calculator_package.zip .
  artifacts:
    paths:
      - build/calculator_package.zip
  tags:
    - ubuntu
```

---

Этот формат позволяет легко читать и понимать структуру проекта, а также настраивать и запускать его на различных платформах.
