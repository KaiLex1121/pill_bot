from app.models.database import Advertisment

class AdSearchText:

    cancel_ad_search: str = "Отменить поиск и вернуться в главное меню?"

    @staticmethod
    def show_search_preview(
        city: str,
        drugs: str,
    ) -> str:

        text = f"""
<b>Это превью твоего поискового запроса. Здесь можно посмотреть его параметры и изменить их (в будущем, коненчно) </b>

<b>Город:</b> {city}
<b>Лекарства:</b> {drugs}
"""
        return text

    @staticmethod
    def show_ad_text(ad: Advertisment) -> str:
        text = f"""
<b>Город:</b> {ad.city}
<b>Лекарства:</b> {ad.drugs}
<b>Способ доставки:</b> {ad.delivery_type.value}
<b>Дополнительная информация:</b> {ad.additional_text}
<b>Контакты пользователя:</b> @{ad.user.username}"""
        return text
