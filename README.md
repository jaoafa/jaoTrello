# jaoTrello

[jao Minecraft Server](https://jaoafa.com) で一部の運営処理用に使用している [Trello](https://trello.com/) の自動管理を行うシステムのプロジェクトです。

## ✨ 機能 ✨

### カードが作成されたとき

カードは原則 `❓状況未確認` か `👀発見` のいずれかで作成されます。

- カードが `❓状況未確認` か `👀発見` のいずれかで作成されたときは、設置破壊数を説明文に追記します。
- カードが `❓状況未確認` で作成されたときは、カードタイトルのユーザーが行った設置破壊マップを画像ファイル `map.png` として添付します。

### カードが変更されたとき (カードが移動したときなど)

- カードが `👀発見` に移動したときに、`map.png` ファイルが添付されていたら、その添付ファイルを削除します。
- カードが `❓状況未確認` か `👀発見` のいずれかに移動したときは、設置破壊数を説明文に追記します。
- カードが `🚧作業中` か `✅完了` のいずれかに移動したときは、移動したユーザーをカードメンバーに追加します。ただし、`✅完了` に移動した際にメンバーが誰か入っていた場合は処理しません。

### カードに添付ファイルが追加されたとき

カードに添付ファイルが追加されたときは、「利用者によって荒らし箇所が発見され、証拠となるスクリーンショットが添付されたとき」です。

- カードが `❓状況未確認` にある場合は、`👀発見` に移動します。この際、添付されたファイルのファイル名が `map.png` であった場合は実施しません。

### カードにラベルが追加されたとき

カードにラベルが追加されたときは、「処罰の種類が決定した」ときです。

- カードが `👀発見` にある場合は、`✋処罰種別決定` に移動します。

## カードにメンバーが追加されたとき

カードにメンバーが追加されたときは、「処罰の処理を実施する運営メンバーが決定したとき」です。

- カードが `✋処罰種別決定` にある場合は、`🚧作業中` に移動します。

## 💣 利用者（運営含む）が実施するべきこと 💣

### 荒らし行為と思われる情報をマップや設置破壊記録のみで見つけたとき

このとき、カードは作成されていません。

- `❓状況未確認` にカードを作成してください。カードのタイトルは荒らしを行ったと思われるユーザーの Minecraft ID だけを記入してください。

### 荒らし行為をサーバ内で発見・確認したとき

このとき、カードは `❓状況未確認` か `👀発見` にあるか、作成されていません。

- カードが作成されていない場合は、 `👀発見` にカードを作成し、証拠となるスクリーンショットを添付してください。
- カードが既に作成されている場合は、証拠となるスクリーンショットをそのカードに添付してください。

カードは自動的に `👀発見` に移動します。

### 運営がカードの内容に対して処罰を決定したとき

このとき、カードは `👀発見` にあります。

- 適用する処罰の種別のラベルを、そのカードに追加してください。

カードは自動的に `✋処罰種別決定` に移動します。

### 運営がカードの内容に対して処罰を実施するとき（対応者が決定したとき）

このとき、カードは `✋処罰種別決定` にあります。

- 対応者に該当するメンバーを、そのカードに追加してください。
- 本人がメンバー追加しても構いません。

カードは自動的に `🚧作業中` に移動します。手動で `🚧作業中` に移動した場合、移動したユーザーがカードメンバーに追加されます。

### 運営がカードの内容に対して処罰を実施し終えたとき（MCBans へのアップロードも成功したとき）

このとき、カードは `🚧作業中` にあります。

- カードを `✅完了` に移動してください。手動で `✅完了` に移動し、またカードメンバーにだれも割り当てられていない場合、移動したユーザーがカードメンバーに追加されます。

### 運営がカードの内容に対して処罰を実施し終えたとき（MCBans へのアップロードが出来なかったとき）

このとき、カードは `🚧作業中` にあります。

- カードを `😅MCBans復旧待ち` に移動してください。

MCBans が復旧したら証拠画像をアップロードし、カードを `✅完了` に移動してください。
