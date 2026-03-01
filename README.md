# ComfyUI Colab Toolkit

> Генерируй AI-видео и фото БЕСПЛАТНО прямо в браузере — без установки, без мощного компьютера, без программирования

[![GitHub Stars](https://img.shields.io/github/stars/russiankendricklamar/comfyui-colab-toolkit?style=social)](https://github.com/russiankendricklamar/comfyui-colab-toolkit/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/russiankendricklamar/comfyui-colab-toolkit/blob/main/notebooks/colab_long_video_setup.ipynb)

---

## Что это такое?

Представь, что у тебя есть волшебная кнопка в браузере. Ты нажимаешь — и через несколько минут получаешь готовое AI-видео или красивый портрет. Никаких установок, никаких настроек, никаких мощных компьютеров. Именно это и есть **ComfyUI Colab Toolkit**.

**Простыми словами:**

Это набор готовых «тетрадок» (notebooks) для сервиса Google Colab. Google Colab — это бесплатный облачный компьютер от Google с мощной видеокартой, которую Google даёт тебе попользоваться прямо в браузере. Наши тетрадки уже настроены и готовы к работе — тебе остаётся только открыть ссылку и нажать кнопку Play.

**Как это работает — шаг за шагом:**

1. Ты открываешь ссылку на тетрадку (кнопка «Open in Colab» выше)
2. Google даёт тебе бесплатную видеокарту NVIDIA T4 (16 ГБ видеопамяти) в облаке
3. Тетрадка автоматически устанавливает всё необходимое прямо на этот облачный компьютер
4. Ты вводишь описание (или загружаешь фото) — и получаешь результат

**Тебе НЕ нужно:**
- Покупать или иметь мощный компьютер
- Покупать видеокарту
- Что-либо устанавливать на свой компьютер
- Знать программирование
- Платить деньги (Colab бесплатный!)

**Что ты сможешь делать:**

- Создавать видео из текстового описания — просто написал «закат на пляже в стиле аниме» и получил видео
- Оживлять фотографии — загрузил фото, оно задвигалось
- Делать «говорящие головы» — фото + голосовое сообщение = человек на фото говорит твоими словами
- Создавать красивые портреты для Instagram в любом стиле
- Переносить художественный стиль с одной картинки на другую
- Снимать вертикальные видео для Reels и TikTok из папки с фотографиями
- Обучать собственную AI-модель на своём лице (15–30 фото) — чтобы генерировать себя в любых ситуациях
- Управлять всем через Telegram-бот — написал в Telegram, получил видео в ответ

---

## Возможности

| Функция | Описание | Тетрадка |
|---|---|---|
| **Text to Video** (Wan 2.2 14B) | Опиши видео словами — получи видео длиной до 30 секунд | `colab_long_video_setup` |
| **Image to Video** (Wan 2.2) | Загружи фотографию — модель оживит её, добавив реалистичное движение | `colab_long_video_setup` |
| **Video to Video** (Wan 2.2) | Возьми готовое видео и измени его стиль — аниме, масляная живопись и т.д. | `colab_long_video_setup` |
| **Talking Head** (Wan 2.2 + FantasyTalking) | Фото + аудио = человек на фото говорит с синхронизацией губ | `colab_long_video_setup` |
| **Reels / TikTok** (Wan 2.2) | Папка с фотографиями → вертикальные видео для соцсетей | `colab_wan_video` |
| **Photo Portraits** (Flux Dev) | Instagram-качество FaceID портреты в любых образах | `colab_flux_photo` |
| **Style Transfer** (Flux + IPAdapter) | Перенеси стиль с референс-картинки на новую генерацию | `colab_flux_photo` |
| **LoRA Training** (ai-toolkit) | Обучи AI на своё лицо (15–30 фото, ~1 час) | `colab_lora_training` |
| **HunyuanVideo** (альтернатива) | В 2 раза быстрее Wan, модель 7.76 ГБ | `colab_hunyuan_video` |
| **CogVideoX** (альтернатива) | Кинематографический стиль, самая лёгкая модель (~5 ГБ) | `colab_cogvideo` |
| **Telegram Bot** | Пиши промпт в Telegram — получай видео прямо в чат | `colab_long_video_setup` |
| **Post-Processing** | Апскейл 480p → 1080p, интерполяция 24 → 48 fps | `colab_long_video_setup` |
| **Google Drive** | Автосохранение результатов на Drive | все ноутбуки |
| **VRAM Monitor** | Мониторинг видеопамяти GPU в реальном времени | `colab_long_video_setup` |

---

## Что нужно?

**Обязательно:**

- **Аккаунт Google** — для доступа к Google Colab и Google Drive. Если есть Gmail — аккаунт уже есть. Регистрация бесплатная на [accounts.google.com](https://accounts.google.com)
- **Любой браузер** — Chrome, Firefox, Safari, Edge — подойдёт любой

**По желанию:**

- **Аккаунт Telegram** — только если хочешь использовать Telegram-бота
- **15–30 своих фотографий** — только если хочешь обучить LoRA на своё лицо

**Точно НЕ нужно:**

- Мощный компьютер или ноутбук — вся работа на серверах Google
- Видеокарта (GPU) — Google даёт NVIDIA T4 бесплатно
- Установка чего-либо на компьютер
- Знания программирования
- Деньги — Google Colab полностью бесплатен

---

## Какие ноутбуки есть

| Ноутбук | Что делает | Запустить |
|---|---|---|
| `colab_long_video_setup.ipynb` | **ГЛАВНЫЙ.** Wan 2.2 14B — полный комбайн: автонастройка GPU, 6 видео-воркфлоу, постобработка (480p→1080p + 24→48fps), пакетная генерация, Google Drive, VRAM-монитор, **Telegram-бот** с русскими инлайн-кнопками. **С него и начинайте.** | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/russiankendricklamar/comfyui-colab-toolkit/blob/main/notebooks/colab_long_video_setup.ipynb) |
| `colab_wan_video.ipynb` | Облегчённая версия Wan. Все 6 воркфлоу, но без бота и постобработки. Добавлены: TTS для talking head, Qwen2-VL промпт-энхансер, видеомонтаж. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/russiankendricklamar/comfyui-colab-toolkit/blob/main/notebooks/colab_wan_video.ipynb) |
| `colab_flux_photo.ipynb` | Flux Dev fp8 — фотопортреты. FaceID (одно лицо в разных образах) + img2img перенос стиля. Выход: 864x1080. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/russiankendricklamar/comfyui-colab-toolkit/blob/main/notebooks/colab_flux_photo.ipynb) |
| `colab_lora_training.ipynb` | Обучение LoRA на своё лицо через ai-toolkit. 15–30 фото → 30–60 мин → файл для Flux. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/russiankendricklamar/comfyui-colab-toolkit/blob/main/notebooks/colab_lora_training.ipynb) |
| `colab_hunyuan_video.ipynb` | HunyuanVideo 1.5 (Tencent) — в 2 раза быстрее Wan, модель 7.76 ГБ. 848x480 при 16fps. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/russiankendricklamar/comfyui-colab-toolkit/blob/main/notebooks/colab_hunyuan_video.ipynb) |
| `colab_cogvideo.ipynb` | CogVideoX-5B — самая лёгкая модель (~5 ГБ). Кинематографичная эстетика. T2V + I2V. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/russiankendricklamar/comfyui-colab-toolkit/blob/main/notebooks/colab_cogvideo.ipynb) |
| `colab_telegram_bot.ipynb` | Отдельный Telegram-бот (проще, чем в главном). Команды: `/photo`, `/text`, `/talking`, `/v2v`. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/russiankendricklamar/comfyui-colab-toolkit/blob/main/notebooks/colab_telegram_bot.ipynb) |

---

### Какой ноутбук выбрать?

- **«Хочу всё и сразу — видео, бот, постобработку, Drive?»**
  → [`colab_long_video_setup.ipynb`](https://colab.research.google.com/github/russiankendricklamar/comfyui-colab-toolkit/blob/main/notebooks/colab_long_video_setup.ipynb) *(главный, рекомендуется всем)*

- **«Хочу быстро сделать видео без лишнего?»**
  → [`colab_wan_video.ipynb`](https://colab.research.google.com/github/russiankendricklamar/comfyui-colab-toolkit/blob/main/notebooks/colab_wan_video.ipynb)

- **«Хочу фото-портреты с моим лицом?»**
  → [`colab_flux_photo.ipynb`](https://colab.research.google.com/github/russiankendricklamar/comfyui-colab-toolkit/blob/main/notebooks/colab_flux_photo.ipynb)

- **«Хочу обучить AI на своё лицо?»**
  → [`colab_lora_training.ipynb`](https://colab.research.google.com/github/russiankendricklamar/comfyui-colab-toolkit/blob/main/notebooks/colab_lora_training.ipynb)

- **«Wan слишком медленный?»**
  → [`colab_hunyuan_video.ipynb`](https://colab.research.google.com/github/russiankendricklamar/comfyui-colab-toolkit/blob/main/notebooks/colab_hunyuan_video.ipynb) *(быстрее, 7.76 ГБ)* или [`colab_cogvideo.ipynb`](https://colab.research.google.com/github/russiankendricklamar/comfyui-colab-toolkit/blob/main/notebooks/colab_cogvideo.ipynb) *(самый лёгкий, ~5 ГБ)*

- **«Хочу управлять через Telegram?»**
  → [`colab_long_video_setup.ipynb`](https://colab.research.google.com/github/russiankendricklamar/comfyui-colab-toolkit/blob/main/notebooks/colab_long_video_setup.ipynb) *(лучший бот, инлайн-кнопки)* или [`colab_telegram_bot.ipynb`](https://colab.research.google.com/github/russiankendricklamar/comfyui-colab-toolkit/blob/main/notebooks/colab_telegram_bot.ipynb) *(проще, команды)*

---

## Быстрый старт (5 минут)

> Инструкция для тех, кто открывает ComfyUI впервые. Никаких установок. Никаких платёжных карт. Всё на серверах Google, бесплатно.

### Шаг 1. Открыть ноутбук

Нажмите на кнопку — она откроет главный ноутбук прямо в браузере:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/russiankendricklamar/comfyui-colab-toolkit/blob/main/notebooks/colab_long_video_setup.ipynb)

Если появится предупреждение "This notebook was not authored by Google" — это нормально. Нажмите **"Run anyway"**.

### Шаг 2. Разобраться с интерфейсом

Вы увидите страницу, разбитую на блоки — они называются **ячейки** (cells). Каждая ячейка — это отдельный кусок кода или текста. Слева от каждой ячейки есть кнопка Play ▶.

Вам не нужно понимать, что написано внутри ячеек. Достаточно их запустить.

### Шаг 3. Запустить всё одной кнопкой

В верхнем меню нажмите:

```
Runtime → Run all
```

Или нажмите **Ctrl+F9** (Windows/Linux) / **Cmd+F9** (Mac).

Это запустит все ячейки по порядку. Colab сам подключится к GPU, установит ComfyUI, скачает модели и запустит сервер.

### Шаг 4. Подождать установку (~5–10 минут)

Будет скачиваться около **28 ГБ** моделей. Бегущие строчки логов — это нормально. Просто следите, чтобы не было красных ошибок.

> Важно: не закрывайте вкладку и не переводите компьютер в сон.

### Шаг 5. Найти ссылку на ComfyUI

В выводе одной из ячеек появится ссылка вида:

```
https://xxxxxxxx.trycloudflare.com
```

**Нажмите на неё** — откроется интерфейс ComfyUI в новой вкладке.

### Шаг 6. Загрузить воркфлоу

В ComfyUI нажмите **"Load"** (правый верхний угол) и выберите воркфлоу, например:

- `video_wan_long_ultimate.json` — универсальный, для старта

### Шаг 7. Загрузить фото или написать промпт

- **Image-to-Video:** найдите узел "Load Image" и загрузите фото
- **Text-to-Video:** найдите текстовое поле и напишите описание

Пример: `a young woman walking through a neon-lit Tokyo street at night, cinematic, 4k`

### Шаг 8. Запустить генерацию

Нажмите **"Queue Prompt"**. Ждите **2–15 минут**.

### Шаг 9. Найти готовое видео

Видео сохраняется в `/content/ComfyUI/output/`. Найдите его в файловом менеджере Colab (иконка папки слева).

### Шаг 10. Сохранить на Google Drive

Запустите ячейку **"Save to Drive"** — она скопирует результаты в папку `MyDrive/ComfyUI_Output/`.

---

## Подробные гайды

### 1. Wan 2.2 — Главный ноутбук (`colab_long_video_setup.ipynb`)

Самый полный ноутбук. 17 ячеек, покрывает весь цикл: установка → генерация → постобработка → Telegram.

#### Группы ячеек

**Ячейки 1–5: Установка**

- **Ячейка 1** — Проверка GPU. Если GPU не подключён: `Среда выполнения → Сменить тип → GPU → T4`
- **Ячейка 2** — Автоконфигурация под ваш GPU (T4/L4/A100)
- **Ячейка 3** — Установка ComfyUI
- **Ячейка 4** — Установка расширений (WanVideoWrapper, VideoHelperSuite, KJNodes, Impact-Pack, RIFE)
- **Ячейка 5** — SageAttention (ускорение ~30%, опционально)

**Ячейка 6: Загрузка моделей**

Интерактивные чекбоксы — выберите нужные модели:

| Модель | Размер | Назначение | Обязательна? |
|---|---|---|---|
| Wan 2.2 T2V 14B fp8 | ~9.5 ГБ | Основная модель генерации | Да |
| VACE Module 14B | ~5 ГБ | Длинные видео (I2V, >81 кадра) | Для длинных видео |
| UMT5 XXL Text Encoder fp8 | ~4.9 ГБ | Понимание текстовых промптов | Да |
| Wan VAE | ~200 МБ | Кодировщик изображений | Да |
| RealESRGAN x4plus | ~64 МБ | Апскейл видео (x2/x4) | Нет |
| RIFE v4.6 | ~115 МБ | Интерполяция кадров | Нет (авто) |

**Ячейка 7:** Загрузка воркфлоу из GitHub
**Ячейка 8:** Запуск ComfyUI + Cloudflare туннель

#### Режимы генерации

| Режим | Файл воркфлоу | Вход | Выход | Время на T4 |
|---|---|---|---|---|
| Длинное видео (I2V) | `video_wan_long_ultimate` | Фото + текст | До 30 сек | 5–15 мин |
| Текст в видео (T2V) | `video_wan_t2v` | Только текст | 3–10 сек | 2–5 мин |
| Короткий клип | `video_wan_clip` | Фото + текст | 3.4 сек | 2–3 мин |
| Видео в видео (V2V) | `video_wan_v2v` | Видео + текст | Рестайлинг | 5–10 мин |
| Talking Head | `video_wan_talking` | Фото + аудио | Говорящий | 3–5 мин |
| Reels | `video_wan_reels` | Папка фото | Вертикальное | 3–5 мин |

#### Длительность видео

| Кадры (frames) | Длительность | Время на T4 |
|---|---|---|
| 81 | 3.4 сек | 2–3 мин |
| 241 | 10 сек | 4–6 мин |
| 481 | 20 сек | 8–12 мин |
| 721 | 30 сек | 12–20 мин |

> Совет: начинайте с 81 или 241, чтобы быстро проверить результат. Для 481+ нужен модуль VACE.

#### Разрешения

| Разрешение | Соотношение | Для чего |
|---|---|---|
| 832x480 | 16:9 | YouTube, горизонтальный |
| 480x832 | 9:16 | Reels, TikTok, Stories |
| 608x1080 | 9:16 HD | Вертикальный, выше качество |

**Ячейка 9:** Документация
**Ячейка 10:** Синхронизация с Google Drive
**Ячейка 11:** Постобработка (апскейл + интерполяция + экспорт)
**Ячейка 12:** Пакетная генерация (список промптов → автоматическая очередь)
**Ячейка 13:** VRAM-монитор
**Ячейка 14:** Оптимизация (кеш моделей, TeaCache, настройки по GPU)
**Ячейки 15–16:** Telegram-бот (подробнее ниже)

---

### 2. Wan 2.2 — Лёгкий (`colab_wan_video.ipynb`)

Те же воркфлоу Wan 2.2, но без постобработки, пакетной генерации и Telegram-бота. Быстрее запускается.

**Дополнительные возможности:**

- **TTS (edge-tts)** — синтез речи для Talking Head прямо в ноутбуке
- **Qwen2-VL** — загрузи фото, модель сама опишет его и сформирует промпт
- **Видеомонтаж** — склейка нескольких клипов в один ролик

**Когда использовать:** хочешь быстро попробовать без бота и Drive.

---

### 3. Flux Photo (`colab_flux_photo.ipynb`)

Генерация фотографий с Flux Dev. Два воркфлоу:

#### `photo_flux_instagram` — Портреты FaceID

Генерирует фото с вашим лицом в разных образах, сохраняя узнаваемость.

1. Загрузите 3 папки с референсами: `portrait`, `hall`, `street`
2. IPAdapter FaceID анализирует черты лица
3. Задайте промпт → получите фото с вашим лицом в новой обстановке

**Выход:** 864x1080 (идеально для Instagram)

#### `photo_flux_img2img` — Перенос стиля

1. Загрузите одно референсное изображение
2. IPAdapter переносит стиль на новую генерацию
3. Настройте `denoise`: 0.65 = мягко, 0.9 = сильно

**Модели:** ~18 ГБ (Flux Dev fp8 + CLIP Vision + IPAdapter FaceID + IPAdapter Flux)

Есть ячейка **"Download LoRA"** — загрузка с Drive или по URL.

---

### 4. LoRA Training (`colab_lora_training.ipynb`)

#### Что такое LoRA?

LoRA — это небольшой файл (50–200 МБ), который «дообучает» нейросеть на вашем лице. Загрузили 20 фото, подождали час — и модель навсегда знает, как вы выглядите.

#### Процесс

**Шаг 1: Подготовьте 15–30 фотографий**

- Разные ракурсы: анфас, три четверти, профиль
- Разное освещение: день, вечер, лампа
- Разная одежда и выражения лица
- Не используйте: солнечные очки, маски, фильтры

**Шаг 2: Задайте триггер-слово** (по умолчанию `ohwx`)

**Шаг 3: Настройте** — 1000–2000 шагов, 30–60 мин на T4

**Шаг 4: Запустите обучение** → получите `.safetensors` файл

**Шаг 5: Используйте в Flux** — добавьте ноду `LoraLoader`, используйте триггер в промпте:
```
photo of ohwx person, standing in a park, cinematic lighting
```

---

### 5. HunyuanVideo 1.5 (`colab_hunyuan_video.ipynb`)

Альтернатива Wan от Tencent — быстрее и легче.

| Параметр | Wan 2.2 | HunyuanVideo 1.5 |
|---|---|---|
| Размер модели | ~14 ГБ | ~7.76 ГБ |
| Скорость | Базовая | ~в 2 раза быстрее |
| Качество | Наилучшее | Хорошее |
| FPS | 24 | 16 |
| Разрешение | 832x480 | 848x480 |
| Лучше для | Финальный результат | Быстрые итерации |

**Когда использовать:** тестируете промпты, нужна скорость, VRAM на пределе.

---

### 6. CogVideoX-5B (`colab_cogvideo.ipynb`)

Самая лёгкая модель с кинематографическим стилем.

| Параметр | Wan 2.2 | CogVideoX-5B |
|---|---|---|
| Размер модели | ~14 ГБ | ~5 ГБ |
| Скорость | Базовая | Самая быстрая |
| Эстетика | Реалистичная | Кинематографическая |
| FPS | 24 | 8 |
| Разрешение | 832x480 | 720x480 |
| Лучше для | Реалистичное видео | Стилизованный контент |

Поддерживает T2V и I2V. Для плавности используйте RIFE из главного ноутбука.

---

### 7. Telegram-бот

Управляй генерацией прямо из Telegram!

#### Вариант A: Встроенный бот (главный ноутбук, ячейки 15–16) — Рекомендуется

- Полная автоматизация: отправил промпт → получил видео
- Русский интерфейс с инлайн-кнопками
- Пошаговый диалог: режим → фото → промпт → длительность → ориентация
- Очередь до 10 задач
- Автопостобработка (апскейл + интерполяция)
- Автосохранение на Drive
- Вайтлист по Telegram ID

#### Вариант B: Отдельный ноутбук (`colab_telegram_bot.ipynb`)

- Проще, управление командами: `/photo`, `/text`, `/talking`, `/v2v`
- Менее автоматизирован

#### Как настроить бота

**Шаг 1: Создайте бота**
1. Откройте `@BotFather` в Telegram
2. Напишите `/newbot`
3. Придумайте имя (например: `My Video Bot`)
4. Придумайте username (например: `myvideo_bot`)
5. Получите **токен**: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

> Храните токен в тайне!

**Шаг 2: Узнайте свой ID**
1. Напишите `@userinfobot` в Telegram
2. Он ответит числом вида `987654321`

**Шаг 3: Запустите ячейку 15** — вставьте токен и ID

**Шаг 4: Запустите ячейку 16** — бот стартует

**Шаг 5:** Откройте бота в Telegram, нажмите `/start`

---

## Workflows — что это и как использовать

Workflow — это файл с настройками, который говорит ComfyUI что делать: какую модель загрузить, какое разрешение, сколько кадров. Вы загружаете файл и нажимаете кнопку — никакого программирования.

### Все воркфлоу

| Файл | Модель | Тип | Вход | Выход | Примечания |
|---|---|---|---|---|---|
| `video_wan_long_ultimate.json` | Wan 2.2 + VACE | I2V | фото + текст | до 30 сек | Главный, лучшее качество |
| `video_wan_t2v.json` | Wan 2.2 | T2V | текст | 3–10 сек | Только текст |
| `video_wan_clip.json` | Wan 2.2 | I2V | фото + текст | 3.4 сек | Короткий клип |
| `video_wan_v2v.json` | Wan 2.2 + VACE | V2V | видео + текст | рестайлинг | Сохраняет движение |
| `video_wan_talking.json` | Wan 2.2 + FantasyTalking | Talking | фото + аудио | говорящий | Lip sync |
| `video_wan_reels.json` | Wan 2.2 | I2V | папки фото | вертикальное | Локальные пути (Mac) |
| `video_wan_reels_colab.json` | Wan 2.2 | I2V | папки фото | вертикальное | Пути Colab |
| `video_hunyuan_t2v.json` | HunyuanVideo 1.5 | T2V | текст | 4–8 сек | 2x быстрее Wan |
| `video_cogvideo_t2v.json` | CogVideoX-5B | T2V | текст | ~6 сек | Кинематографический |
| `photo_flux_instagram.json` | Flux + FaceID | Photo | фото лица + текст | портрет | Локальные пути |
| `photo_flux_instagram_colab.json` | Flux + FaceID | Photo | фото лица + текст | портрет | Пути Colab |
| `photo_flux_img2img.json` | Flux + IPAdapter | Photo | референс + текст | стилизованное | Перенос стиля |

> Воркфлоу с `_colab` в названии — для Colab. Без суффикса — для локальной установки.

### Как загрузить воркфлоу

1. Откройте ComfyUI в браузере по ссылке-туннелю
2. Нажмите на иконку меню (левый верхний угол)
3. Нажмите **"Load"**
4. Выберите `.json` файл
5. Воркфлоу появится на холсте
6. Измените промпт/настройки если нужно
7. Нажмите **"Queue Prompt"**

---

## Куда сохраняются результаты

### 1. Сервер Colab (временно)

**Путь:** `/content/ComfyUI/output/`

Это **временное** хранилище. Все файлы **удаляются**, когда сессия Colab завершается. Всегда сохраняйте на Drive!

### 2. Google Drive (постоянно)

**Путь:** `Мой диск / ComfyUI_Output/`

Файлы остаются навсегда. Доступны с телефона и компьютера через [drive.google.com](https://drive.google.com).

> Внимание: бесплатный Google Drive — 15 ГБ. Следите за заполненностью.

### 3. Telegram (через бот)

Бот отправляет видео прямо в чат. Видео >50 МБ сохраняются на Drive (лимит Telegram).

### Схема

```
Генерация ComfyUI
       |
       v
/content/ComfyUI/output/ (временно, на сервере)
       |
       +--> Google Drive (постоянно, ComfyUI_Output/)
       |
       +--> Telegram (бот отправляет в чат)
       |
       +--> Скачать вручную (File → Download)
```

---

## Пост-обработка

Сырое видео из ComfyUI — 480p при 24fps. Постобработка делает его лучше.

### 1. Апскейл (RealESRGAN x4)

- **480p → 1080p** (x2) или **480p → 4K** (x4)
- AI-улучшение — не просто растягивание пикселей
- Время: **2–5 минут**

### 2. Интерполяция кадров (RIFE)

- **24fps → 48fps** или **60fps**
- AI генерирует промежуточные кадры — движение становится плавным
- Время: **1–3 минуты**

### 3. Экспорт

| Формат | Когда использовать |
|---|---|
| `mp4` | Везде — соцсети, мессенджеры, монтаж **(рекомендуется)** |
| `webm` | Веб-сайты, меньший размер |
| `gif` | Мемы, без звука, большой размер |

**Где доступна:** ячейка 11 главного ноутбука (ручной запуск) или автоматически через Telegram-бот.

---

## FAQ / Частые проблемы

### «Out of memory» / «CUDA out of memory»

GPU закончилась видеопамять. Решения по порядку:

1. Запустите `clear_vram()` из ячейки Optimization Toolkit
2. Уменьшите разрешение: `480x320` вместо `832x480`
3. Уменьшите кадры: `81` (3 сек) вместо `481` (20 сек)
4. Увеличьте `blocks_to_swap` до `30` в WanVideoWrapper
5. Перезапустите: **Runtime → Restart runtime**

### «Colab отключился / Session crashed»

Бесплатный Colab имеет лимиты:
- Макс. сессия: ~12 часов
- Таймаут простоя: ~90 минут
- Дневная квота GPU: ограничена

**Решения:**
- Держите вкладку активной
- Сохраняйте на Drive регулярно
- Используйте кеш моделей (ячейка 14) — следующий запуск в секунды

### «Видео плохого качества»

- Запустите постобработку (апскейл + интерполяция)
- Увеличьте steps с 20 до 25–30
- Снизьте CFG до 5.0–5.5 (меньше перенасыщения)
- Пишите конкретные промпты: освещение, ракурс, стиль
- TeaCache — только для черновиков

### «Бот не отвечает»

1. Ячейка 16 всё ещё выполняется? (в выводе "Bot is running!")
2. Ваш user ID в вайтлисте? (ячейка 15)
3. ComfyUI запущен? (ячейка 8, ссылка-туннель активна)
4. Попробуйте `/cancel`, затем `/start`
5. Не помогает: перезапустите runtime, запустите всё заново

### «Модели долго скачиваются»

Первый раз: ~28 ГБ, 10–20 минут. Это нормально.

**Решение:** активируйте кеш моделей (ячейка 14). Модели сохранятся на Drive и восстановятся мгновенно в следующий раз.

### «Tunnel URL не работает»

1. Подождите 30 секунд, попробуйте снова
2. Перезапустите ячейку 8
3. Если повторяется: **Runtime → Restart runtime**

---

## Ограничения

| Ограничение | Значение | Примечания |
|---|---|---|
| Максимальная сессия | ~12 часов | Бесплатный Colab |
| Таймаут простоя | ~90 минут | Держите вкладку активной |
| Память GPU | 16 ГБ (T4) | `blocks_to_swap` для больших моделей |
| Макс. длина видео | 30 сек (721 кадр) | 832x480 на T4 |
| Время генерации | 2–20 минут | Зависит от длины и разрешения |
| Лимит Telegram | 50 МБ | Крупные файлы → Drive |
| Google Drive free | 15 ГБ | Следите за хранилищем |
| Квота GPU | Ограничена | Google может ограничить |

---

## Лицензия

MIT License — свободное использование, модификация и распространение.
