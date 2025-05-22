#下書き機能

import Component.component_def as component_def
import Database.crud_draft as crud_draft


async def draft_save(ctx, text):
    user_id, guild_id = await component_def.return_user_data(ctx)

    text = await crud_draft.draft_text_add(user_id, guild_id, text)

    await component_def.message_response_ephemeral(ctx, text)


async def draft_check(ctx):

    user_id, guild_id = await component_def.return_user_data(ctx)

    draft = await crud_draft.draft_text_check(user_id, guild_id)
    print(draft)

    text = ""
    for i, d in enumerate(draft):
        text += f"{i+1}.\n"
        if len(d.text) >= 300:
            draft_text = f"{d.text[0:300]}..."
        else:
            draft_text = d.text
        text += f"{draft_text}\n\n"

    if draft != []:

        text += "\n下書の全文を確認するためには、コマンド'/draft 下書番号'を実行してください"
    
    else:
        text += "保存された下書はありません"

    await component_def.message_response_ephemeral(ctx, text)


async def draft(ctx, number):

    user_id, guild_id = await component_def.return_user_data(ctx)

    draft = await crud_draft.draft_text_selected(user_id, guild_id)

    try:

        text = f"```{draft[number-1].text}```"

    except:

        text = "下書の取得に失敗しました"
        
    finally:

        await component_def.message_response_ephemeral(ctx, text)


async def draft_delete(ctx, number):
    user_id, guild_id = await component_def.return_user_data(ctx)

    isDeleteDraft = await crud_draft.draft_text_delete(user_id, guild_id, number)

    if isDeleteDraft:
        text = "選択した下書を削除しました"
    else:
        text = "選択した下書の削除に失敗しました"

    await component_def.message_response_ephemeral(ctx, text)