# Created by ay27 at 15/01/2018
import os
import time

CMD1 = 'nvidia-smi| grep MiB | grep -v Default'
CMD2 = 'ps -eo pid,user | grep {}'


def kill(user, pid):
    print('kill pid {}'.format(pid))
    os.system('kill -9 {}'.format(pid))
    log = 'time {} kill {} pid={}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), user, pid)
    os.popen('echo "{}" >> /home/ay27/gpu.log'.format(log))


def scan():
    pid2gid = dict()
    user2pid = dict()
    user2gid = dict()
    pid2user = dict()

    processes = os.popen(CMD1).read().split('\n')
    for p in processes:
        if len(p.split()) != 7:
            continue
        _, gpu_id, pid, ptype, pname, memory, _ = p.split()

        user = os.popen(CMD2.format(pid)).read().split('\n')
        for u in user:
            _pid, _u = u.split()
            if pid == _pid:
                user = _u
                break

        if user not in user2pid:
            user2pid[user] = set()
        user2pid[user].add(pid)

        if user not in user2gid:
            user2gid[user] = set()
        user2gid[user].add(gpu_id)

        if pid not in pid2gid:
            pid2gid[pid] = set()
        pid2gid[pid].add(gpu_id)

        pid2user[pid] = user

    for u in user2pid:
        log = '{} user {}, pid {}, gid {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                                                  u, user2pid[u], user2gid[u])
        os.popen('echo "{}" >> /home/ay27/gpu.log'.format(log))
        print(log)
    return pid2gid, user2gid, user2pid, pid2user


if __name__ == '__main__':

    pid2gid, user2gid, user2pid, pid2user = scan()

    for p in pid2gid:
        if len(pid2gid[p]) > 2:
            kill(pid2user[p], p)

    for u in user2pid:
        if len(user2gid[u]) > 4:
            print('kill user {}'.format(u))
            for p in user2pid[u]:
                kill(u, p)
