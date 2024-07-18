import os
import shutil
import subprocess
import sys
import platform
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from .colors import bcolors

CHROME = [
    '{8A69D345-D564-463c-AFF1-A69D9E530F96}',
    '{8237E44A-0054-442C-B6B6-EA0509993955}',
    '{401C381F-E0DE-4B85-8BD8-3F3F14FBDA57}',
    '{4ea16ac7-fd5a-47c3-875b-dbf4a2008c20}'
]

def download_driver(patched_drivers):
    osname = platform.system()

    print(bcolors.WARNING + 'Getting Chrome Driver...' + bcolors.ENDC)

    if osname == 'Linux':
        osname = 'lin'
        exe_name = ""
        with subprocess.Popen(['google-chrome-stable', '--version'], stdout=subprocess.PIPE) as proc:
            version = proc.stdout.read().decode('utf-8').replace('Google Chrome', '').strip()
    elif osname == 'Darwin':
        osname = 'mac'
        exe_name = ""
        process = subprocess.Popen(
            ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'], stdout=subprocess.PIPE)
        version = process.communicate()[0].decode(
            'UTF-8').replace('Google Chrome', '').strip()
    elif osname == 'Windows':
        osname = 'win'
        exe_name = ".exe"
        version = None
        try:
            process = subprocess.Popen(
                ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
            )
            version = process.communicate()[0].decode(
                'UTF-8').strip().split()[-1]
        except Exception:
            for i in CHROME:
                for j in ['opv', 'pv']:
                    try:
                        command = [
                            'reg', 'query', f'HKEY_LOCAL_MACHINE\\Software\\Google\\Update\\Clients\\{i}', '/v', f'{j}', '/reg:32']
                        process = subprocess.Popen(
                            command,
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
                        )
                        version = process.communicate()[0].decode(
                            'UTF-8').strip().split()[-1]
                    except Exception:
                        pass

        if not version:
            print(bcolors.WARNING +
                  "Couldn't find your Google Chrome version automatically!" + bcolors.ENDC)
            version = input(bcolors.WARNING +
                            'Please input your google chrome version (ex: 91.0.4472.114) : ' + bcolors.ENDC)
    else:
        input('{} OS is not supported.'.format(osname))
        sys.exit()

    try:
        with open('version.txt', 'r') as f:
            previous_version = f.read()
    except Exception:
        previous_version = '0'

    with open('version.txt', 'w') as f:
        f.write(version)

    if version != previous_version:
        try:
            os.remove(f'chromedriver{exe_name}')
        except Exception:
            pass

        shutil.rmtree(patched_drivers, ignore_errors=True)

    # Install ChromeDriver using ChromeDriverManager
    driver_path = ChromeDriverManager().install()

    # Move the downloaded driver to patched_drivers directory
    os.makedirs(patched_drivers, exist_ok=True)
    destination = os.path.join(patched_drivers, f'chromedriver{exe_name}')
    shutil.move(driver_path, destination)

    return osname, exe_name, destination


def copy_drivers(cwd, patched_drivers, exe, total):
    current = os.path.join(patched_drivers, f'chromedriver{exe}')
    os.makedirs(patched_drivers, exist_ok=True)
    for i in range(total+1):
        try:
            destination = os.path.join(
                patched_drivers, f'chromedriver_{i}{exe}')
            shutil.copy(current, destination)
        except Exception:
            pass
