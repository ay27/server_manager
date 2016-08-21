#!/usr/bin/python3
# Created by ay27 at 16/8/18

import argparse
import subprocess
import sys, os
from notebook.auth import passwd
import urllib.request

config = """
c.NotebookApp.ip='*'
c.NotebookApp.password = u'%s'
c.NotebookApp.open_browser = False
c.NotebookApp.port = 10002 """


def run_cmd(cmd, show_msg=False, waite=True):
    # print(cmd)
    if not show_msg:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        p = subprocess.Popen(cmd, shell=True)
    if waite:
        out, err = p.communicate()
        rc = p.returncode
        return out, err, rc


class DesktopAction:
    choices = ['start', 'stop', 'restart']

    def call(self, values):
        if values == DesktopAction.choices[0]:
            self.start()
        elif values == DesktopAction.choices[1]:
            self.stop()
        elif values == DesktopAction.choices[2]:
            self.restart()
            # elif values == DesktopAction.choices[3]:
            #     self.delete()

    def start(self):
        self.stop()
        geometry = os.environ.get('GEOMETRY')
        if geometry is None:
            geometry = '1366x768'
        run_cmd('export USER=root && vncserver -depth 24 -geometry %s :1' % geometry, show_msg=True)
        run_cmd("sed -i 's/-solid grey$/-solid grey -cursor_name left_ptr/g' /root/.vnc/xstartup")
        run_cmd('/etc/init.d/xrdp start')

        out1, err1, rc1 = run_cmd('netstat -nlatp | grep 10001| grep -v grep')
        out2, err2, rc2 = run_cmd('netstat -nlatp | grep 5900| grep -v grep')
        if out1 is not None and out2 is not None and rc1 == rc2 == 0:
            print('start service success')
        else:
            print('start service error')

            run_cmd('/etc/init.d/xrdp stop')
            run_cmd('vncserver -kill :1')
            run_cmd('ps -ef|grep xrdp|grep -v grep|cut -c 9-15|xargs kill -9')
            run_cmd('rm -rf /var/run/xrdp* /tmp.X1-lock /tmp/.X11-unix/X1')

    def stop(self):
        run_cmd('/etc/init.d/xrdp stop')
        run_cmd('vncserver -kill :1')
        run_cmd('ps -ef|grep xrdp|grep -v grep|cut -c 9-15|xargs kill -9')
        run_cmd('rm -rf /var/run/xrdp* /tmp.X1-lock /tmp/.X11-unix/X1')

        out1, err1, rc1 = run_cmd('netstat -nlatp | grep 0.0.0.0:10001')
        out2, err2, rc2 = run_cmd('netstat -nlatp | grep 0.0.0.0:5900')
        if rc1 == rc2 == 1:
            print('stop service success')
        else:
            print('stop service error')

    def restart(self):
        self.start()

        # def delete(self):
        #     self.stop()
        #     run_cmd('rm -rf /root/.Xauthority /root/.vnc/*')
        #     out1, err1, rc1 = run_cmd('ls -al /root/| grep .vnc| grep -v grep')
        #     out2, err2, rc2 = run_cmd('ls -al /root/| grep .Xauthority| grep -v grep')
        #     if rc1 == rc2 == 1:
        #         print('all configuration has been deleted')
        #     else:
        #         print('delete configuration failed')


class JupyterAction:
    choices = ['start', 'stop', 'del']

    def call(self, values):
        if values == JupyterAction.choices[0]:
            self.start()
        elif values == JupyterAction.choices[1]:
            self.stop()
        elif values == JupyterAction.choices[2]:
            self.delete()

    def start(self):
        self.stop()
        print('please input the password to access jupyter')
        sha1 = passwd()
        run_cmd('mkdir /root/.jupyter')
        run_cmd('rm /root/.jupyter/jupyter_notebook_config.py')
        with open('/root/.jupyter/jupyter_notebook_config.py', 'w') as f:
            f.write(config % sha1)
        run_cmd('screen -dmS jupyter -s jupyter-notebook', waite=False)

        out1, err1, rc1 = run_cmd('netstat -nlatp | grep 0.0.0.0:10002')
        if rc1 == 0 and len(out1) > 0:
            print('start jupyter server success')
        else:
            print('start jupyter error')

    def stop(self):
        run_cmd('ps -ef|grep jupyter-notebook|grep -v grep|cut -c 9-15|xargs kill -9')
        run_cmd('screen -wipe')

        out1, err1, rc1 = run_cmd('netstat -nlatp | grep 0.0.0.0:10002')
        if rc1 == 1:
            print('stop jupyter server success')
        else:
            print('stop jupyter error')

    def delete(self):
        self.stop()
        run_cmd('rm -f /root/.jupyter/jupyter_notebook_config.py')
        print('delete configuration success')


class UpdateAction:
    def call(self, values):
        if values:
            self.do_update()

    def do_update(self):
        # check version
        out, err, rc = run_cmd('cat /root/.manager_version')
        if rc == 0 and len(out) > 0:
            old_version = int(out)
        else:
            old_version = 0

        # fetch newest version
        url = urllib.request.urlopen('https://raw.githubusercontent.com/ay27/server_manager/master/version_tag')
        newest_version = int(url.read().decode('utf-8'))
        if old_version >= newest_version:
            print('current version is newest, nothing to do')
            sys.exit(0)
        else:
            print('current version is %d, the newest version is %d' % (old_version, newest_version))
            run_cmd('rm -rf /root/.server_manager')
            run_cmd('git clone https://github.com/ay27/server_manager.git /root/.server_manager', show_msg=True)
            run_cmd('cd /root/.server_manager && ./install', show_msg=True)
            print('update finish!')


if __name__ == '__main__':
    # out = passwd()
    # print(out)

    parser = argparse.ArgumentParser(prog='platform manager')
    sub_parser = parser.add_subparsers(help='optional action')

    desktop_parser = sub_parser.add_parser('desktop', help="manage remote desktop service")

    desktop_parser.add_argument('desktop_action', choices=DesktopAction.choices,
                                help='choose one optional action')

    jupyter_parser = sub_parser.add_parser('jupyter', help="manage jupyter web interface")

    jupyter_parser.add_argument('jupyter_action', choices=JupyterAction.choices,
                                help='choose one optional action')

    update_parser = sub_parser.add_parser('update', help="update manager")
    update_parser.set_defaults(update=True)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(-1)

    args = parser.parse_args()
    vv = vars(args)
    # print(vv)
    if 'desktop_action' in vv.keys():
        if len(sys.argv) < 3:
            desktop_parser.print_help()
        else:
            DesktopAction().call(vv['desktop_action'])
    elif 'jupyter_action' in vv.keys():
        if len(sys.argv) < 3:
            jupyter_parser.print_help()
        else:
            JupyterAction().call(vv['jupyter_action'])
    elif 'update' in vv.keys():
        UpdateAction().call(vv['update'])
