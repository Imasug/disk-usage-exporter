from prometheus_client import start_http_server, Gauge
from pathlib import Path
import time
import argparse


def get_disk_usage(path: Path) -> float:
    return sum(p.stat().st_size for p in path.glob('**/*') if p.is_file())


def get_metrics() -> None:
    for path in paths:
        report_disk_usage(path, get_disk_usage(path))


def report_disk_usage(path: Path, disk_usage: float) -> None:
    disk_usage_gauge.labels(path).set(disk_usage)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path', nargs='+', help="the target paths scraped for disk usage", type=Path)
    parser.add_argument(
        '-i', '--interval', help="the minutes of scrape interval", type=float, default=1.0)
    args = parser.parse_args()

    paths = args.path
    interval = args.interval

    for path in paths:
        assert path.exists()

    disk_usage_gauge = Gauge('node_disk_usage_bytes',
                             'Disk usage of the directory/file. Note that this is not synchronized. The value is scraped by own timer', ['path'])

    start_http_server(9100)

    while True:
        get_metrics()
        # The process is so expensive that metrics is scraped by own timer.
        time.sleep(interval * 60)
