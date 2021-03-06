#!/usr/bin/python3
# Created by ay27 at 16/8/18

import argparse
import subprocess
import sys, os
from time import sleep
from notebook.auth import passwd
import requests
from bs4 import BeautifulSoup, Tag

config = """
c.NotebookApp.ip='*'
c.NotebookApp.password = u'%s'
c.NotebookApp.open_browser = False
c.NotebookApp.port = 10002
c.NotebookApp.allow_root = True """

downgrad_pip = 'wget https://pypi.python.org/packages/e7/a8/7556133689add8d1a54c0b14aeff0acb03c64707ce100ecd53934da1aa13/pip-8.1.2.tar.gz --no-check-certificate;\
 tar -xzvf pip-8.1.2.tar.gz; cd pip-8.1.2;  python setup.py install; cd ..; rm -rf pip-8.1.2 pip-8.1.2.tar.gz'


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

        sleep(1)
        out1, err1, rc1 = run_cmd('netstat -nlatp | grep 10001')
        out2, err2, rc2 = run_cmd('netstat -nlatp | grep 5900')
        if len(out1) > 0 and len(out2) > 0 and rc1 == rc2 == 0:
            print('start service success')
        else:
            print('start service error')

            run_cmd('/etc/init.d/xrdp stop')
            run_cmd('vncserver -kill :1')
            run_cmd('ps -ef|grep xrdp|grep -v grep|cut -c 9-15|xargs kill -9')
            run_cmd('rm -rf /var/run/xrdp* /tmp/.X1-lock /tmp/.X11-unix/X1')

    def stop(self):
        run_cmd('/etc/init.d/xrdp stop')
        run_cmd('vncserver -kill :1')
        run_cmd('ps -ef|grep xrdp|grep -v grep|cut -c 9-15|xargs kill -9')
        run_cmd('rm -rf /var/run/xrdp* /tmp/.X1-lock /tmp/.X11-unix/X1')

        sleep(1)
        out1, err1, rc1 = run_cmd('netstat -nlatp | grep 0.0.0.0:10001')
        out2, err2, rc2 = run_cmd('netstat -nlatp | grep 0.0.0.0:5900')
        if rc1 == rc2 == 1:
            print('stop service success')
        else:
            print('stop service error')

    def restart(self):
        self.start()


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

        sleep(3)
        out1, err1, rc1 = run_cmd('netstat -nlatp | grep 0.0.0.0:10002')
        if rc1 == 0 and len(out1) > 0:
            print('start jupyter server success')
        else:
            print('start jupyter error')

    def stop(self):
        run_cmd('ps -ef|grep jupyter-notebook|grep -v grep|cut -c 9-15|xargs kill -9')
        run_cmd('screen -wipe')

        sleep(1)
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

        print('checking if there has new updates')

        newest_version = 0
        link = ''
        try:
            release_page = requests.get('https://github.com/ay27/server_manager/releases')
            soup = BeautifulSoup(release_page.text, "lxml")

            for tag in soup.find_all('div'):
                if tag.attrs.get('class') == ['release', 'label-latest']:
                    for child in tag.find_all('span'):
                        if child.attrs.get('class') == ['css-truncate-target']:
                            newest_version = child.string
                            for div in tag.find_all('div'):
                                if div.attrs.get('class') == ['release-body', 'commit', 'open']:
                                    rows = div.ul.find_all('li')
                                    if len(rows) != 2:
                                        raise Exception('parse download link error')
                                    link = 'https://github.com' + rows[1].a.attrs.get('href')
                                    # print(newest_version)
        except Exception as e:
            print(e)
        # print(newest_version)
        # print(link)

        newest_version = int(newest_version)
        if old_version >= newest_version:
            print('current version is newest, nothing to do')
            sys.exit(0)
        else:
            print('current version is %d, the newest version is %d' % (old_version, newest_version))

            read = input('update now? [y|n]  ')
            read = read.strip()
            while (read != 'y') and (read != 'n'):
                read = input('update now? [y|n]  ')
                read = read.strip()

            if read == 'n':
                sys.exit(0)

            run_cmd('wget -O manager_latest.tar.gz ' + link, show_msg=True)
            dir_name, err, rc = run_cmd('tar -tf manager_latest.tar.gz')
            dir_name = dir_name.decode(encoding='utf-8')
            dir_name = str(dir_name.split('\n')[0])
            run_cmd('tar -xzf manager_latest.tar.gz; rm manager_latest.tar.gz')
            run_cmd('cd %s && ./install' % dir_name, show_msg=True)
            run_cmd('rm -rf %s' % dir_name, show_msg=True)
            print('update finish!')


class FixPipAction:
    def call(self, values):
        if values:
            self.do_fix_pip()

    def do_fix_pip(self):
        run_cmd(downgrad_pip, True)


if __name__ == '__main__':
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

    fix_pip_error_parser = sub_parser.add_parser('fix_pip', help='fix pip error')
    fix_pip_error_parser.set_defaults(fix_pip=True)

    parser.add_argument('-v', '--version', action='store_true', help="version")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(-1)

    args = parser.parse_args()
    vv = vars(args)
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
    elif 'fix_pip' in vv.keys():
        FixPipAction().call(vv['fix_pip'])
    elif 'version' in vv.keys():
        out, err, rc = run_cmd('cat /root/.manager_version')
        if rc == 0:
            print('current version is %s' % out.strip().decode())
        else:
            print("can not found the version file, please run 'manager update' to catch up the newest version")
