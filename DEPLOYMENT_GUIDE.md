# Deployment Guide / Инструкция по развёртыванию

Проект: AI-Платформа для личностного роста  
Версия v0.1.0  
Дата: 19.05.2026

---

# Содержание

1. [Требования](#требования)
2. [Локальный запуск (Docker)](#локальный-запуск-docker)
3. [Локальный запуск (без Docker)](#локальный-запуск-без-docker)
4. [Развёртывание на Yandex Cloud](#развёртывание-на-yandex-cloud)
5. [Проверка работоспособности](#проверка-работоспособности)
6. [Устранение проблем](#устранение-проблем)

---

# Требования

| Компонент | Версия |
|-----------|--------|
| Docker | 20.10+ |
| Docker Compose | 2.0+ |
| Python (без Docker) | 3.11+ |
| Node.js (без Docker) | 18+ |
| PostgreSQL (без Docker) | 15+ |


```bash
git clone https://github.com/ashwanipassi09-ui/ai-personal-growth-platform.git
cd ai-personal-growth-platform
