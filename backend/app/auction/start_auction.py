import sys

from auction_manager import auction_manager

if __name__ == '__main__':
    auction_id = sys.argv[1]
    auction_manager.start_auction_command(id=auction_id)
