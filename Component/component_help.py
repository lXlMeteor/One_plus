#ヘルプコマンド(登録コマンドの出力)機能

import Component.component_def as component_def

async def help(ctx, bot):

    commands = bot.tree.get_commands()  # 登録されたコマンドを取得

    print(commands)

    if commands:

        text = "登録されているコマンド一覧:\n"
        for command in commands:
            command_name = command.name
            
            if hasattr(command, "description") and command.description is not None:
                command_description = command.description
            else:
                command_description = "説明なし"

            text += f"- ```/{command_name}```: {command_description}\n"
        
    else:
        text = "登録されているコマンドがありません。"

    await component_def.message_response_ephemeral(ctx, text)
