import json
import threading

import uvicorn
from fastapi import FastAPI, Request
from trello import TrelloClient

from src import actions, config

client = TrelloClient(
    api_key=config.TRELLO_API_KEY,
    api_secret=config.TRELLO_API_SECRET
)

app = FastAPI()


@app.head("/")
async def head_trello_webhook():
    """
    HEADリクエスト時に受付
    """


@app.post("/")
async def post_trello_webhook(request: Request):
    """
    POSTリクエスト時に受付
    """
    result = await request.json()
    print("POST", result["action"]["type"], json.dumps(result))
    if result["action"]["type"] == "createCard":
        actions.card_created(result)
    if result["action"]["type"] == "updateCard":
        actions.card_updated(result)
    if result["action"]["type"] == "addAttachmentToCard":
        actions.card_added_file(result)
    if result["action"]["type"] == "addLabelToCard":
        actions.card_added_label(result)
    if result["action"]["type"] == "addMemberToCard":
        actions.card_added_member(result)


@app.on_event("startup")
async def startup_event():
    """
    FastAPIのスタートアップ時
    """
    t = threading.Timer(5, register_webhook)
    t.start()


def register_webhook():
    """
    Webhookを登録 (FastAPIのスタートアップから5秒後に呼び出し)
    """
    board = client.get_board(config.TRELLO_BOARD_ID)
    if board is None:
        print("[Error] board not found")
        exit(1)

    for hook in client.list_hooks():
        if hook.callback_url == config.ROOT_WEBHOOK_URL:
            hook.delete()

    webhook = client.create_hook(callback_url=config.ROOT_WEBHOOK_URL, id_model=board.id)
    if not webhook:
        print("failed webhook register")
        exit(1)


if __name__ == "__main__":
    # noinspection PyTypeChecker
    uvicorn.run(app, host="0.0.0.0", port=6668)
