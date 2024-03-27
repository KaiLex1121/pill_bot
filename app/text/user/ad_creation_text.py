from enums.advertisment.ad_type import TypeOfAd
from enums.advertisment.delivery_type import TypeOfDelivery

class AdCreationText:

    @staticmethod
    def show_ad_preview(
        ad_type: TypeOfAd,
        city: str,
        drugs: str,
        delivery_type: TypeOfDelivery,
        additional_text: str | None
    ) -> str:

        if ad_type ==

        text = f"""
        <b>Тип объявления: {ad_type}</b>
        """