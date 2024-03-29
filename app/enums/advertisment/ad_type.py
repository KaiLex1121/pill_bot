import enum


class TypeOfAd(enum.Enum):
    take = 'Ищу'
    give = 'Отдам'


#  TypeOfAd.take.name == take
#  TypeOfAd.take.value == Ищу
