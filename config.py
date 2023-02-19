# ------------------------配置区域------------------------
# 在下方填入cookie,多个账号请输入多个cookie,一行一个:
# 或者也可以填写账号密码,格式为 账号#密码
ck = """

"""

# 下面设置需要执行的任务,True为执行,False为不执行
执行签到任务 = True
执行点赞任务 = True
执行打赏任务 = True

# 下方填写推送方式,二选一,建议用pushplus,不填则不推送
Server酱_key = ''  # https://sct.ftqq.com/
pushplus_key = ''  # https://www.pushplus.plus/
# ------------------------配置区域------------------------

ver = '2.1'
ck = list(filter(None, ck.split('\n')))
