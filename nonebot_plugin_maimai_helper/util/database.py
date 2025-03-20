import sqlite3
import os
from nonebot.log import logger

# 获取数据库文件路径
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'maimai.db')

def init_db():
    """初始化数据库"""
    # 确保data目录存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        # 创建id表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS id (
            qq TEXT PRIMARY KEY,
            userid TEXT NOT NULL
        )
        ''')
        # 创建diving表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS diving (
            qq TEXT PRIMARY KEY,
            token TEXT NOT NULL
        )
        ''')
        conn.commit()
        logger.success("数据库初始化成功")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
    finally:
        conn.close()

def is_userid_exist(user_qq):
    """检查用户ID是否存在"""
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM id WHERE qq = ?', (user_qq,))
        result = cursor.fetchone()
        return result is not None
    except Exception as e:
        logger.error(f"查询用户ID失败: {e}")
        return False
    finally:
        conn.close()

def del_user_id(user_qq, user_id):
    """删除用户ID"""
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM id WHERE qq = ?', (user_qq,))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"删除用户ID失败: {e}")
        return False
    finally:
        conn.close()

def save_user_id(user_qq, user_id):
    """保存用户ID"""
    conn = sqlite3.connect(DB_PATH)
    try:
        if not is_userid_exist(user_qq):
            cursor = conn.cursor()
            cursor.execute('INSERT INTO id (qq, userid) VALUES (?, ?)', (user_qq, user_id))
            conn.commit()
            return 1
        return -1
    except Exception as e:
        logger.error(f"保存用户ID失败: {e}")
        return -2
    finally:
        conn.close()

def get_userid(user_qq):
    """获取用户ID"""
    conn = sqlite3.connect(DB_PATH)
    try:
        if is_userid_exist(user_qq):
            cursor = conn.cursor()
            cursor.execute('SELECT userid FROM id WHERE qq = ?', (user_qq,))
            result = cursor.fetchone()
            if result:
                return result[0]
        return -1
    except Exception as e:
        logger.error(f"获取用户ID失败: {e}")
        return -1
    finally:
        conn.close()

def is_token_exist(user_qq):
    """检查token是否存在"""
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM diving WHERE qq = ?', (user_qq,))
        result = cursor.fetchone()
        return result is not None
    except Exception as e:
        logger.error(f"查询token失败: {e}")
        return False
    finally:
        conn.close()

def save_user_token(user_qq, token):
    """保存用户token"""
    conn = sqlite3.connect(DB_PATH)
    try:
        if not is_token_exist(user_qq):
            cursor = conn.cursor()
            cursor.execute('INSERT INTO diving (qq, token) VALUES (?, ?)', (user_qq, token))
            conn.commit()
            return 1
        return -1
    except Exception as e:
        logger.error(f"保存token失败: {e}")
        return -2
    finally:
        conn.close()

def get_token(user_qq):
    """获取用户token"""
    conn = sqlite3.connect(DB_PATH)
    try:
        if is_token_exist(user_qq):
            cursor = conn.cursor()
            cursor.execute('SELECT token FROM diving WHERE qq = ?', (user_qq,))
            result = cursor.fetchone()
            if result:
                return result[0]
        return -1
    except Exception as e:
        logger.error(f"获取token失败: {e}")
        return -1
    finally:
        conn.close() 