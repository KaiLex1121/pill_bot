from app.models.database import Advertisment


class AdSearchText:

    cancel_ad_search: str = "Отменить поиск и вернуться в главное меню?"

    @staticmethod
    def show_search_preview(
        country: str,
        city: str,
        drugs: str,
    ) -> str:

        text = f"""
<b>Это превью твоего поискового запроса. Здесь можно посмотреть его параметры и изменить их (в будущем, коненчно) </b>

<b>Страна:</b> {country}
<b>Город:</b> {city}
<b>Лекарства:</b> {drugs}
"""
        return text

    @staticmethod
    def show_ad_text(ad: Advertisment) -> str:
        text = f"""
Я <b>{ad.ad_type.value.lower()}</b> таблеточки
<b>Город:</b> {ad.city}
<b>Лекарства:</b> {ad.drugs}
<b>Способ доставки:</b> {ad.delivery_type.value.lower()}
<b>Дополнительная информация:</b> {ad.additional_text}
<b>Контакты пользователя:</b> @{ad.user.username}

<b> Дата создания объявления:</b> {ad.created_at.strftime('%d.%m.%y')}"""
        return text
