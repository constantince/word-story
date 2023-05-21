import mysql.connector
import hashlib
from datetime import datetime

cnx = mysql.connector.connect(
    user='words',
    password='hBccx2M3GW6MrtmN',
    host='localhost',
    database='words'
)

def generate_id(email):
    # 将邮箱转换为字节串
    email_bytes = email.encode('utf-8')
  
    # 使用MD5哈希算法对字节串进行哈希处理
    md5_hash = hashlib.md5()
    md5_hash.update(email_bytes)
    id = md5_hash.hexdigest()

    return id

def generate_date():
    # 获取当前日期和时间
    now = datetime.now()
    datetime_str = now.strftime("%Y/%m/%d %H:%M:%S")
    return datetime_str
    
def generate_pin(words):
    # 计算文本的SHA-256哈希值
    hash_object = hashlib.sha256(words.encode())

    # 将哈希值转换为16进制字符串表示
    hex_digest = hash_object.hexdigest()

    # 取前10位字符作为唯一的10位字符串
    unique_string = hex_digest[:10]

    return unique_string
    
def login(email, password):
    print(email, password)
    # 定义插入数据的 SQL 语句
    sql = "SELECT * FROM `words`.`user` WHERE email = %s AND password = %s"
    val = (email, password)
   
    # 创建游标对象
    mycursor = cnx.cursor()
    
    # 执行操作
    formatted_sql = mycursor.execute(sql, val)
    print(formatted_sql)
    try:
        return mycursor.fetchall()
         
    except mysql.connector.Error as err:
        return []
        
    
    # 输出插入结果信息
    cursor.close()
    cnx.close()

def createUser(email, password):

    user = generate_id(email)
    d = generate_date()
    # 定义插入数据的 SQL 语句
    #INSERT INTO `aiamzplus`.`amz-plus-user` (`id`, `user`, `password`, `email`, `type`, `openkey`) VALUES (NULL, 'XXXXX', 'HYX6TEJK9', 'xyz.com', '3', '')
    sql = "INSERT INTO `words`.`user` (`uid`, `password`, `email`, `create_time`) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE uid = %s"
    val = (user, password, email, d, user)
    
    # 创建游标对象
    mycursor = cnx.cursor()
    
    mycursor.execute(sql, val)
    # 提交数据库事务
    cnx.commit()
    
    # 输出插入结果信息
    mycursor.close()
    
    return mycursor.rowcount

def createStory(uid, words):
    d = generate_date()
    p = generate_pin(words)
    # 定义插入数据的 SQL 语句
    #INSERT INTO `aiamzplus`.`amz-plus-user` (`id`, `user`, `password`, `email`, `type`, `openkey`) VALUES (NULL, 'XXXXX', 'HYX6TEJK9', 'xyz.com', '3', '')
    sql = "INSERT INTO `words`.`stories` (`uid`, `words`, `pin`, `status`, `create_time`) VALUES (%s, %s, %s, %s, %s)"
    val = (uid, words, p, 0, d)
    
    # 创建游标对象
    mycursor = cnx.cursor()
    
    mycursor.execute(sql, val)
    # 提交数据库事务
    cnx.commit()
    
    # 输出插入结果信息
    mycursor.close()
    
    return mycursor.rowcount

def updateStory(uid, content, status):
     # 创建一个游标对象，用于执行SQL查询
    cursor = cnx.cursor()

    # 构建更新语句
    update_query = f"UPDATE `words`.`stories` SET content = %s, status = %s WHERE uid = %s"

    # 执行更新操作
    cursor.execute(update_query, (content, stattus, uid))

    # 提交更改到数据库
    cnx.commit()

    # 关闭游标和连接
    cursor.close()
    cnx.close()

if __name__ == '__main__':
    # createUser("alberteinsteion007@126.com", "afDb13rf5byu8")
    # createStory("6bca9c198f44dd96be85", "speak,look,specification")
    updateStory("6bca9c198f44dd96be85", "<b>dfdfdfdfdf</b>", 1)
