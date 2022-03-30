import argparse
from loader import load_html
from repair import BeautifulSoupRepair
from parser import HTMLTree
from main_info import MeaningTree


def extract_main_info(url: str) -> str:
    html_string = load_html(url)
    repaired = BeautifulSoupRepair(html_string).repaired()
    tree = HTMLTree(repaired)
    info_list = MeaningTree(tree).main_info()
    return '\n'.join(info_list)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', dest='url', type=str)

    args = parser.parse_args()
    if not args.url:
        raise AttributeError

    print(extract_main_info(args.url))


if __name__ == '__main__':
    main()
