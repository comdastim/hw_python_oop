
class InfoMessage:
    """Cамостоятельный класс для создания объектов сообщений."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """
        Возвращает строку сообщения о типе и длительности тренировки,
        потраченных калориях, дистанции и средней скорости спортсмена.
        """
        message: str = (f'Тип тренировки: {self.training_type};'
                        f' Длительность: {self.duration:.3f} ч.;'
                        f' Дистанция: {self.distance:.3f} км;'
                        f' Ср. скорость: {self.speed:.3f} км/ч;'
                        f' Потрачено ккал: {self.calories:.3f}.')
        return message


class Training:
    """Базовый класс тренировки, который содержит
       основные свойства и методы для видов тренировок.
    """
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Возвращает дистанцию (в километрах), которую преодолел спортсмен."""
        distance: float = (self.action * self.LEN_STEP / self.M_IN_KM)
        return distance

    def get_mean_speed(self) -> float:
        """Возвращает среднюю скорость движения спортсмена."""
        distance: float = self.get_distance()
        speed: float = distance / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Возвращает количество потраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Возвращает информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """
    Тренировка: бег.
    """
    MIN_IN_HR: int = 60
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SUBTRAHEND = 20

    def get_spent_calories(self) -> float:
        calories: float = (((self.CALORIES_MEAN_SPEED_MULTIPLIER
                           * self.get_mean_speed()
                           - self.CALORIES_MEAN_SPEED_SUBTRAHEND)
                           * self.weight / self.M_IN_KM
                           * self.duration) * self.MIN_IN_HR)
        return calories


class SportsWalking(Training):
    """
    Тренировка: спортивная ходьба.
    """
    MIN_IN_HOUR: int = 60
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    SPEED_HEIGHT_QUOTIENT_MULTIPLIER: float = 0.029
    CALORIES_SPEED_EXPONENT = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:

        calories: float = ((self.CALORIES_WEIGHT_MULTIPLIER
                           * self.weight
                           + (self.get_mean_speed()
                            ** self.CALORIES_SPEED_EXPONENT // self.height)
                           * self.SPEED_HEIGHT_QUOTIENT_MULTIPLIER
                           * self.weight)
                           * self.duration * self.MIN_IN_HOUR)
        return calories


class Swimming(Training):
    """
    Тренировка: плавание.
    """
    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SUMMAND = 1.1
    CALORIES_SUM_MULTIPLIER = 2

    def __init__(self,
                 action,
                 duration,
                 weight,
                 count_pool: float,
                 length_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.count_pool = count_pool
        self.length_pool = length_pool

    def get_mean_speed(self) -> float:
        """Возвращает среднюю скорость, с которой плывет спорстмен."""
        speed: float = (self.length_pool * self.count_pool
                        / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        """Возвращает количество потраченных пловцом калорий."""
        calories: float = ((self.get_mean_speed()
                           + self.CALORIES_MEAN_SPEED_SUMMAND)
                           * self.CALORIES_SUM_MULTIPLIER * self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Распаковывает пакеты данных, полученные от датчиков."""
    packages_dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type in packages_dict.keys():
        return packages_dict[workout_type](*data)
    else:
        raise ValueError


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
