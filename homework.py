from dataclasses import dataclass
from typing import List


@dataclass
class InfoData:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type, duration,
                 distance, speed, calories) -> None:

        self.info_data = InfoData(training_type, duration,
                                  distance, speed, calories)

    def get_message(self) -> str:
        message = ((f'Тип тренировки: {self.info_data.training_type}; '
                    f'Длительность: {self.info_data.duration:.3f} ч.; '
                    f'Дистанция: {self.info_data.distance:.3f} км; '
                    f'Ср. скорость: {self.info_data.speed:.3f} км/ч; '
                    f'Потрачено ккал: {self.info_data.calories:.3f}.'))
        return message


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    HOUR_IN_MIN: int = 60

    def __init__(self,
                 action: int,           # количество совершённых действий
                 duration: float,       # длительность тренировки
                 weight: float,         # вес спортсмена
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.training_type = ""

    # расчёт дистанции, которую пользователь преодолел за тренировку:
    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        result: float

        result = self.action * self.LEN_STEP / self.M_IN_KM

        return result

    # расчёт средней скорости движения во время тренировки:
    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        result: float

        distance = self.get_distance()
        result = distance / self.duration

        return result

    # расчёт количества потраченных калорий за тренировку:
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        if self.training_type.__class__ is not self.__class__:
            return NotImplementedError()

    # создание объекта сообщения о результатах тренировки:
    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = ((InfoMessage(self.training_type, self.duration,
                self.get_distance(), self.get_mean_speed(),
                self.get_spent_calories())))

        return info


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIES_1: int = 18
    COEFF_CALORIES_2: int = 20

    def __init__(self, action, duration, weight):
        super().__init__(action, duration, weight)
        self.training_type = __class__.__name__

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        result: float
        hour_in_min = self.duration * self.HOUR_IN_MIN

        result = ((self.COEFF_CALORIES_1
                  * self.get_mean_speed()
                  - self.COEFF_CALORIES_2)
                  * self.weight / self.M_IN_KM * hour_in_min)

        return result


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIES_1: float = 0.035
    COEFF_CALORIES_2: float = 0.029

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.training_type = __class__.__name__
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        result: float

        result = ((self.COEFF_CALORIES_1 * self.weight
                  + (self.get_mean_speed() ** 2 // self.height)
                  * self.COEFF_CALORIES_2 * self.weight)
                  * (self.duration * self.HOUR_IN_MIN))

        return result


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_CALORIES_1: float = 1.1
    COEFF_CALORIES_2: float = 2

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.training_type = __class__.__name__
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        result: float

        result = (((self.length_pool * self.count_pool
                    / self.M_IN_KM / self.duration)))

        return result

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        result: float

        result = ((self.get_mean_speed() + self.COEFF_CALORIES_1)
                  * self.COEFF_CALORIES_2 * self.weight)

        return result


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    codes_type = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking
    }
    if workout_type in codes_type:
        return codes_type[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    if training is None:
        print(f"Такой тип {workout_type} - не предусмотрен программой!")
    else:
        info_message = training.show_training_info()
        print(info_message.get_message())


if __name__ == '__main__':
    packages = [
        ('ЕWM', [720, 1, 80, 25, 40]),
        ('RUN', [1206, 12, 6]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
