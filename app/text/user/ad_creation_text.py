from app.enums.advertisment.ad_type import TypeOfAd
from app.enums.advertisment.delivery_type import TypeOfDelivery


class AdCreationText:

    cancel_ad_creating: str = "Отменить создание объявления и вернуться в главное меню?"

    @staticmethod
    def show_ad_preview(
        ad_type: TypeOfAd,
        city: str,
        drugs: str,
        delivery_type: TypeOfDelivery,
        additional_text: str | None,
        username: str | None
    ) -> str:

        text = f"""
<b>Превью анкеты. Здесь можно посмотреть ее параметры и изменить их (в будущем, коненчно) </b>

<b>Я:</b> {ad_type} лекарство
<b>Город:</b> {city}
<b>Лекарства:</b> {drugs}
<b>Способ доставки:</b> {delivery_type}
<b>Дополнительная информация:</b> {additional_text}
<b>Мой контакт:</b> @{username}
"""
        return text
