# ewvkqq-sdk

An unofficial Python SDK for querying and monitoring orders on `910.ewvkqq.cn`.

The project provides two modes:

- **Pull mode**: one-shot API requests (fetch order list, order detail, and shop info).
- **Poll mode**: continuous polling with callback-based event handling.

> ⚠️ This repository is **unofficial** and interacts with a third-party service. Use it at your own risk and comply with all applicable terms and laws.

## Features

- Automatic session/cookie bootstrap via Playwright.
- CAPTCHA flow integration.
- OCR-based CAPTCHA text recognition through local Ollama model (`glm-ocr`).
- Threaded polling decorator for event-driven monitoring.
- Simple examples for both pull and poll workflows.

## Project Structure

- `ewvkqq/pull.py`: pull-style APIs (`order`, `order_info`, `shop_info`) and retry wrapper.
- `ewvkqq/poll.py`: poll-style event registration and background thread loop.
- `ewvkqq/utils.py`: shared config, HTTP session, auth logic, and utilities.
- `pull_example.py`: bulk fetch and export account card data to `account.json`.
- `poll_example.py`: monitor new paid orders and print detail payloads.

## Requirements

- Python 3.9+
- [Ollama](https://ollama.com/) running locally
- OCR model available in Ollama: `glm-ocr`
- Playwright browser runtime installed

Python packages used by the code:

- `requests`
- `playwright`
- `opencv-python`
- `numpy`
- `ollama`

## Installation

```bash
pip install requests playwright opencv-python numpy ollama
python -m playwright install chromium
```

## Quick Start

### 1) Pull mode (single request)

```python
from ewvkqq import pull

# Query paid orders by contact keyword
orders = pull.pull_event(pull.Event.order, "123456", 1)
print(orders)
```

### 2) Poll mode (continuous monitoring)

```python
from ewvkqq import poll, run_main

@poll.poll_event(poll.Event.order, "123456", 1)
def on_order(payload: dict):
    if payload.get("code") == 1:
        print(payload)

run_main(delay=1.0)
```

## Examples

Run existing example scripts directly:

```bash
python pull_example.py
python poll_example.py
```

## API Overview

### `ewvkqq.pull.Event`

- `order(contact: str, status: int = 999, current: int = 1, page_size: int = 999) -> dict`
- `order_info(trade_no: str) -> dict`
- `shop_info(token: str) -> dict`

### `ewvkqq.pull.pull_event`

Retry wrapper for pull events with delay controlled by `run_main(delay=...)`/shared config.

### `ewvkqq.poll.Event`

- `order(callback, contact: str, status: int = 999)`

### `ewvkqq.poll.poll_event`

Decorator that registers a callback into a background polling thread.

### `ewvkqq.run_main(delay: float = 0)`

Starts all registered polling threads and blocks until they finish.

## Notes

- CAPTCHA OCR accuracy depends on model quality and image clarity.
- Excessively frequent polling may trigger anti-bot protections.
- Keep your own contact/order data secure.

## License

This project is licensed under the GNU GPL v3 License. See [![license](https://img.shields.io/github/license/rbxluau/ewvkqq-sdk)](https://github.com/rbxluau/ewvkqq-sdk/blob/main/LICENSE).
