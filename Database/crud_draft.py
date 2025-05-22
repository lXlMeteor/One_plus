
from sqlalchemy.future import select
from datetime import datetime
from .base import session
from .models import Draft
import Database.base_def as base_def


async def draft_data_get(db_session, user_id, guild_id):
    data = await db_session.execute(select(Draft).filter(Draft.user_id == user_id, Draft.guild_id == guild_id,\
                                                            Draft.exist == True))
    data = await base_def.get_all(data)

    return data


async def draft_text_add(user_id, guild_id, text):
    async with session()as db_session, db_session.begin():
        try:

            if len(text) > 2000:
                text = "文字数が2000文字を超えているため、保存できません"
                return text
            
            draft = await draft_data_get(db_session, user_id, guild_id)

            if draft and len(draft) >= 3:
                text = "下書の保存量を超えたため、保存できません"
                return text
            
            else:

                draft_data = Draft(user_id = user_id, guild_id = guild_id, text = text, add_time = datetime.now(), exist = True)
                await base_def.db_add(draft_data)

                text = "下書の保存が完了しました"
                return text
            
        except:

            text = "下書の保存に失敗しました"
            return text

async def draft_text_check(user_id, guild_id):
    async with session()as db_session, db_session.begin():

        draft = await draft_data_get(db_session, user_id, guild_id)

        return draft

async def draft_text_selected(user_id, guild_id):
    async with session()as db_session, db_session.begin():
        
        draft = await draft_data_get(db_session, user_id, guild_id)

        return draft

async def draft_text_delete(user_id, guild_id,number):
    try:
        async with session()as db_session, db_session.begin():
            
            draft = await draft_data_get(db_session, user_id, guild_id)

            draft[number-1].exist = False
            await db_session.commit()

            isDeleteDraft = True

            return 
        
    except AttributeError as error:
        print(error)
        isDeleteDraft = False

    finally:
        return isDeleteDraft