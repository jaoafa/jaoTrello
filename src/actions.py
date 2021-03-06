from src import get_place_break_count, get_uuid_from_mcid
from src.__main__ import client

JAOTAN_ID = "5a4c3e874b994a781d05e680"

LIST_IDS = {
    "NOT_CHECKED": "60af2b797a0f72620c62c28b",  # 状況未確認
    "DISCOVER": "60816a7e6791dc5c605fb4e5",  # 発見
    "TYPE_DECISION": "60816a7e6791dc5c605fb4e6",  # 処罰種別決定
    "WORKING": "60816a7e6791dc5c605fb4e7",  # 作業中
    "COMPLETION": "6081744d3edb972b0e3588e5",  # 完了
}


class DummyTrelloUser:
    """
    ダミーの Trello ユーザー
    """
    def __init__(self, user_id: str):
        self.user_id = user_id

    @property
    def id(self):
        """
        このオブジェクトにある Trello ユーザー ID を返す

        :return: Trello ユーザー ID
        """
        return self.user_id


def card_add_place_break(card,
                         uuid):
    """
    カード説明に設置破壊数を追加
    """
    if "reportコマンドによって" in card.description or "設置破壊数:" in card.description:
        return  # 設置破壊数が既に設定されている

    placeCount, breakCount = get_place_break_count(uuid)

    cp_url = "https://admin.jaoafa.com/cp/" + uuid

    if placeCount is not None:
        new_description = card.description + "\n---\n\n- 設置破壊数: Place: " + str(placeCount) + " / Break: " + str(breakCount) + "\n" + cp_url
    else:
        new_description = card.description + "\n---\n\n- 設置破壊数: 取得に失敗しました。\n" + cp_url

    card.set_description(new_description)


def card_add_map_image(card,
                       uuid):
    """
    カードにマップ画像を追加
    """
    for attachment in card.attachments:
        if attachment["name"] == "map.png":
            return  # map.pngが既にある

    card.attach(name="map.png", url="https://api.jaoafa.com/cities/getblockimg?uuid=" + uuid)


def card_remove_map_image(card):
    """
    カードからマップ画像を削除
    """
    for attachment in card.attachments:
        if attachment["name"] == "map.png":
            card.remove_attachment(attachment["id"])


def card_created(json):
    """
    カード作成時に呼び出し

    ・設置破壊数の取得、書き込み (状況未確認・発見時)
    ・マップの添付 (状況未確認のみ)
    ・マップの削除 (発見のみ)
    """
    card_id = json["action"]["data"]["card"]["id"]
    card = client.get_card(card_id)

    if json["action"]["memberCreator"]["id"] == JAOTAN_ID:
        return  # jaotanによるカード作成

    if card.list_id == LIST_IDS["NOT_CHECKED"]:
        # 状況未確認
        uuid = get_uuid_from_mcid(card.name)
        if uuid is None:
            return  # UUIDが取得できなかった

        card_add_place_break(card, uuid)
        card_add_map_image(card, uuid)

    if card.list_id == LIST_IDS["DISCOVER"]:
        # 発見
        uuid = get_uuid_from_mcid(card.name)
        if uuid is None:
            return  # UUIDが取得できなかった

        card_remove_map_image(card)
        card_add_place_break(card, uuid)


def card_updated(json):
    """
    カード変更時に呼び出し

    ・設置破壊数の取得、書き込み (状況未確認・発見時)
    ・マップの削除 (発見のみ)
    """
    card_id = json["action"]["data"]["card"]["id"]
    card = client.get_card(card_id)

    if json["action"]["memberCreator"]["id"] == JAOTAN_ID:
        return  # jaotanによるカード変更

    if card.list_id == LIST_IDS["NOT_CHECKED"]:
        # 状況未確認
        uuid = get_uuid_from_mcid(card.name)
        if uuid is None:
            return  # UUIDが取得できなかった

        card_add_place_break(card, uuid)

    if card.list_id == LIST_IDS["DISCOVER"]:
        # 発見
        uuid = get_uuid_from_mcid(card.name)
        if uuid is None:
            return  # UUIDが取得できなかった

        card_remove_map_image(card)
        card_add_place_break(card, uuid)

    if card.list_id == LIST_IDS["WORKING"]:
        # 作業中 -> メンバー追加
        card.add_member(DummyTrelloUser(json["action"]["memberCreator"]["id"]))

    if card.list_id == LIST_IDS["COMPLETION"] and len(card.idMembers) == 0:
        # 完了 & メンバーが誰も入っていない -> メンバー追加
        card.add_member(DummyTrelloUser(json["action"]["memberCreator"]["id"]))


def card_added_file(json):
    """
    カードにファイルが追加されたときに呼び出し

    ・状況未確認にカードがあるとき、発見に移動 (map.pngを除く)
    """
    card_id = json["action"]["data"]["card"]["id"]
    card = client.get_card(card_id)

    if json["action"]["memberCreator"]["id"] == JAOTAN_ID:
        return  # jaotanによるカード変更

    if card.list_id == LIST_IDS["NOT_CHECKED"]:
        # 状況未確認
        added_filename = json["action"]["data"]["attachment"]["name"]
        if added_filename == "map.png":
            return

        card.change_list(LIST_IDS["DISCOVER"])  # 発見に移動


def card_added_label(json):
    """
    カードにラベルが追加されたとき

    ・発見にカードがあるときのみ、処罰種別決定に移動
    """
    card_id = json["action"]["data"]["card"]["id"]
    card = client.get_card(card_id)

    if json["action"]["memberCreator"]["id"] == JAOTAN_ID:
        return  # jaotanによるカードラベル追加

    if card.list_id == LIST_IDS["DISCOVER"]:
        # 発見
        card.change_list(LIST_IDS["TYPE_DECISION"])  # 処罰種別決定に移動


def card_added_member(json):
    """
    カードにメンバーが追加されたとき

    ・処罰種別決定にカードがあるときのみ、作業中に移動
    """
    card_id = json["action"]["data"]["card"]["id"]
    card = client.get_card(card_id)

    if json["action"]["memberCreator"]["id"] == JAOTAN_ID:
        return  # jaotanによるカードラベル追加

    if card.list_id == LIST_IDS["TYPE_DECISION"]:
        # 処罰種別決定
        card.change_list(LIST_IDS["WORKING"])  # 作業中に移動
