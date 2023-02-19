from api import *


def 签到任务():
    log.success("开始执行签到任务")
    try:
        签到()
        for i in range(4):
            领取签到奖励(str(i))
        return True
    except Exception:
        return False


def 点赞任务():
    try:
        log.success("开始执行点赞任务")
        i = 0
        q = 0
        while i < 10:
            i += 1
            q += 1
            if q > 40:
                log.error("点赞任务执行错误: 数量过多")
                break
            点赞回复(get_id(), q)
            tid = get_id()
            ret = 喜欢帖子(tid, q)
            if ret == 2:
                log.warning(f'tid:{tid}   已取消喜欢,于是重复执行')
                喜欢帖子(tid, q)
            elif ret == 0:
                log.warning(f'tid:{tid}   喜欢失败! 于是任务数量+1')
                i -= 1
        return True
    except Exception:
        return False


def 打赏任务():
    log.success("开始执行打赏任务")
    try:
        if 领取打赏任务奖励()['msg'] == '该任务你已经领取奖励！':
            log.error("打赏任务已经完成!")
            return True
        i = 0
        while i < 3:
            i += 1
            if i > 10:
                log.error("打赏任务执行错误: 数量过多")
                break
            tid = get_id(170000)
            if 打赏帖子(tid, i)['code'] == 0:
                log.warning(f'tid:{tid}   打赏失败! 于是任务数量+1')
                i -= 1
        领取打赏任务奖励()
        return True
    except Exception:
        return False


def 处理经验(经验):
    return int(经验[:经验.find('/')])


def 推送任务(用户名, uid, 喵币, 经验, nck, 签到成功, 点赞成功, 打赏成功):
    log.info(f"第 {nck} 个用户( uid:{uid} 用户名:{用户名})任务结束，开始推送！")
    with open(f'log.log', 'r', encoding='utf-8') as f:
        内容 = f.read()
    try:
        新经验 = 获取经验()
        经验差 = 处理经验(新经验) - 处理经验(经验)
        msg = f'''
        当前用户({nck}): {用户名} ({uid})
        喵币数量: {喵币}
        经验: {新经验} ({处理经验(经验)} + {经验差})
        今日任务执行完毕!
        签到成功: {签到成功}
        点赞成功: {点赞成功}
        打赏成功: {打赏成功}
        
        详细调试信息:
{内容}
        '''
        print(msg)
        if Server酱_key != '':
            Server酱推送(msg)
        if pushplus_key != '':
            pushplus推送(msg)
        return True
    except Exception:
        return False


def 执行用户任务(cookie, nck):
    headers = {
        "cookie": cookie
    }
    s.headers = headers
    签到成功, 点赞成功, 打赏成功 = False, False, False
    try:
        用户名, uid, 喵币, 经验 = 获取用户信息()
    except Exception:
        log.error("获取信息失败")
        return
    if 执行签到任务:
        签到成功 = 签到任务()
        if 签到成功:
            log.success("签到执行任务成功")
        else:
            log.error("签到执行任务失败")
    else:
        log.error("设置不执行签到任务,已跳过")

    if 执行点赞任务:
        点赞成功 = 点赞任务()
        if 点赞成功:
            log.success("点赞任务执行成功")
        else:
            log.error("点赞任务执行失败")
    else:
        log.error("设置不执行点赞任务,已跳过")

    if 执行打赏任务:
        打赏成功 = 打赏任务()
        if 打赏成功:
            log.success("打赏任务执行成功")
        else:
            log.error("打赏任务执行失败")
    else:
        log.error("设置不执行打赏任务,已跳过")

    推送成功 = 推送任务(用户名, uid, 喵币, 经验, nck, 签到成功, 点赞成功, 打赏成功)
    if 推送成功:
        log.success("推送任务执行成功")
    else:
        log.error("推送任务执行失败")


def main():
    log.warning("当前版本为: {ver}".format(ver=ver))
    log.info("m站辅助工具 python版")
    num = 0
    for ckk in ck:
        if '#' in ckk:
            ckk = 登录(ckk[:ckk.find('#')], ckk[ckk.find('#') + 1:])
        log.add('log.log', encoding='utf-8', retention=0)
        num += 1
        log.info(f"当前开始执行第 {num}/{len(ck)} 个用户任务")
        执行用户任务(ckk, f'{num}/{len(ck)}')
    log.info(f'共 {num} 个用户 所有任务执行完毕')


def handler(event, context):
    main()
    return 'success'


if __name__ == '__main__':
    main()
