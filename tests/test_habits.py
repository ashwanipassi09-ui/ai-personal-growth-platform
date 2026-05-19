"""
Автотесты для трекера привычек
Minimum 5 tests as required by checklist #19
"""

import pytest
from datetime import date, timedelta


# ========== Модели для тестирования ==========

class Habit:
    """Модель привычки для тестов"""
    def __init__(self, id, title, frequency, user_id):
        self.id = id
        self.title = title
        self.frequency = frequency  # "daily" или "weekly"
        self.user_id = user_id
        self.streak_current = 0
        self.streak_best = 0
        self.logs = []

    def mark_complete(self, log_date):
        """Отметить привычку как выполненную"""
        self.logs.append({"date": log_date, "completed": True})
        self._update_streak()

    def mark_incomplete(self, log_date):
        """Отметить привычку как невыполненную"""
        self.logs.append({"date": log_date, "completed": False})
        self._update_streak()

    def _update_streak(self):
        """Обновить streak на основе логов"""
        if not self.logs:
            self.streak_current = 0
            return

        # Сортируем логи по дате
        sorted_logs = sorted(self.logs, key=lambda x: x["date"], reverse=True)

        current_streak = 0
        expected_date = date.today()

        for log in sorted_logs:
            if log["completed"] and log["date"] == expected_date:
                current_streak += 1
                expected_date -= timedelta(days=1)
            else:
                break

        self.streak_current = current_streak
        if current_streak > self.streak_best:
            self.streak_best = current_streak

    def get_completion_rate(self, start_date, end_date):
        """Рассчитать процент выполнения за период"""
        logs_in_period = [log for log in self.logs 
                         if start_date <= log["date"] <= end_date]
        if not logs_in_period:
            return 0.0
        completed = sum(1 for log in logs_in_period if log["completed"])
        return (completed / len(logs_in_period)) * 100


# ========== Тест 1: Создание привычки ==========

def test_create_habit():
    """Тест создания новой привычки"""
    habit = Habit(id=1, title="Утренняя медитация", frequency="daily", user_id=101)
    
    assert habit.id == 1
    assert habit.title == "Утренняя медитация"
    assert habit.frequency == "daily"
    assert habit.user_id == 101
    assert habit.streak_current == 0
    assert habit.streak_best == 0
    assert len(habit.logs) == 0


# ========== Тест 2: Отметка выполнения привычки ==========

def test_mark_habit_complete():
    """Тест отметки привычки как выполненной"""
    habit = Habit(id=2, title="Чтение книги", frequency="daily", user_id=102)
    today = date.today()
    
    habit.mark_complete(today)
    
    assert len(habit.logs) == 1
    assert habit.logs[0]["completed"] == True
    assert habit.logs[0]["date"] == today


# ========== Тест 3: Подсчёт streak (серии) ==========

def test_streak_calculation():
    """Тест правильного подсчёта непрерывной серии (streak)"""
    habit = Habit(id=3, title="Зарядка", frequency="daily", user_id=103)
    today = date.today()
    
    # Отмечаем 3 дня подряд
    habit.mark_complete(today)
    habit.mark_complete(today - timedelta(days=1))
    habit.mark_complete(today - timedelta(days=2))
    
    assert habit.streak_current == 3
    assert habit.streak_best == 3


# ========== Тест 4: Streak прерывается при пропуске ==========

def test_streak_breaks_on_miss():
    """Тест: streak должен прерываться при пропуске дня"""
    habit = Habit(id=4, title="Пробежка", frequency="daily", user_id=104)
    today = date.today()
    
    # День 1: выполнено
    habit.mark_complete(today - timedelta(days=2))
    # День 2: пропущено
    habit.mark_incomplete(today - timedelta(days=1))
    # День 3: выполнено
    habit.mark_complete(today)
    
    # Streak должен быть 1 (только сегодняшний день)
    assert habit.streak_current == 1
    # Лучшая серия должна быть 1
    assert habit.streak_best == 1


# ========== Тест 5: Расчёт процента выполнения ==========

def test_completion_rate_calculation():
    """Тест расчёта процента выполнения привычки за период"""
    habit = Habit(id=5, title="Пить воду", frequency="daily", user_id=105)
    today = date.today()
    
    # 3 дня выполнено, 2 дня пропущено
    habit.mark_complete(today - timedelta(days=4))
    habit.mark_complete(today - timedelta(days=3))
    habit.mark_incomplete(today - timedelta(days=2))
    habit.mark_complete(today - timedelta(days=1))
    habit.mark_incomplete(today)
    
    start_date = today - timedelta(days=7)
    end_date = today
    
    rate = habit.get_completion_rate(start_date, end_date)
    
    # 3 выполнено из 5 = 60%
    assert rate == 60.0


# ========== Тест 6 (дополнительный): Лучшая серия сохраняется ==========

def test_best_streak_preserved():
    """Тест: лучшая серия должна сохраняться даже после сброса"""
    habit = Habit(id=6, title="Медитация", frequency="daily", user_id=106)
    today = date.today()
    
    # Первая серия: 5 дней
    for i in range(5):
        habit.mark_complete(today - timedelta(days=i))
    
    assert habit.streak_best == 5
    
    # Пропускаем день
    habit.mark_incomplete(today - timedelta(days=5))
    
    # Новая серия: 2 дня
    habit.mark_complete(today - timedelta(days=6))
    habit.mark_complete(today - timedelta(days=7))
    
    # Лучшая серия должна остаться 5
    assert habit.streak_best == 5


# ========== Тест 7 (дополнительный): Пустая привычка ==========

def test_empty_habit_no_streak():
    """Тест: у новой привычки без логов streak = 0"""
    habit = Habit(id=7, title="Новая привычка", frequency="weekly", user_id=107)
    
    assert habit.streak_current == 0
    assert habit.streak_best == 0
    assert len(habit.logs) == 0
    assert habit.get_completion_rate(date.today(), date.today()) == 0.0
