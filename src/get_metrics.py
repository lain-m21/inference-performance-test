import time
import psutil
import argparse
import threading
import numpy as np


class VegetaWatcher(threading.Thread):
    def __init__(self):
        super(VegetaWatcher, self).__init__()
        self.vegeta_running = False

    def run(self):
        p = None
        while True:
            time.sleep(0.1)
            if p is None:
                p_list = [p for p in psutil.process_iter() if 'vegeta' in set(p.cmdline())]
                if len(p_list) > 0:
                    p = p_list[-1]
                    self.vegeta_running = True
            if p is not None:
                try:
                    p.cpu_percent()
                except:
                    p = None
                    self.vegeta_running = False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--watch',
                        default='tensorflow_model_server',
                        help='Choose either `tensorflow_model_server` or `python`')
    parser.add_argument('--save-path',
                        default='./data/metrics_densenet121_tf_5_5.npy')
    args = parser.parse_args()

    vegeta_watcher = VegetaWatcher()
    vegeta_watcher.start()

    result = []
    flag = False
    while True:
        if not flag and vegeta_watcher.vegeta_running:
            flag = True

        if flag:
            # get cpu metrics
            if args.watch == 'tensorflow_model_server':
                p = [p for p in psutil.process_iter() if 'tensorflow_model_server' in set(p.cmdline())][-1]
            elif args.watch == 'python':
                p = [p for p in psutil.process_iter() if 'python' in set(p.cmdline())][-1]
            else:
                raise ValueError('The watch is invalid')

            cpu_percent = p.cpu_percent()
            cpu_num = p.cpu_num()
            result.append([cpu_percent, cpu_num])

        if flag and not vegeta_watcher.vegeta_running:
            break

    result = np.array(result)
    np.save(args.save_path, result)


if __name__ == '__main__':
    main()
