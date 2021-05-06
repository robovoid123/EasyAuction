import os
import datetime

from auction import Auction
from auction_strategy import AuctionType
from bid import Bid


def run_at(*, command, at):
    date = at.strftime("%H:%M %m/%d/%y")
    FILENAME = 'run_at.txt'

    os.system(f"echo '{command}' > {FILENAME}")

    command = f'at {date} -f {FILENAME}'
    os.system(command)


class AuctionManager:
    _auctions = {}

    @classmethod
    def create_auction(cls, *, product,
                       starting_bid,
                       bid_cap=None,
                       reserve=None,
                       ending_date,
                       auction_type: AuctionType = AuctionType.ENGLISH):
        new_auction = Auction(product=product,
                              starting_bid=starting_bid,
                              bid_cap=bid_cap,
                              ending_date=ending_date,
                              strategy=auction_type
                              )
        if not cls._auctions.get(new_auction.id):
            cls._auctions[new_auction.id] = new_auction
        return new_auction

    @classmethod
    def start_auction(cls, auction_id, starting_date=None):
        auction = cls.get_auction(auction_id)
        if auction:
            if starting_date:
                command = f'python app/auction/start_auction.py {auction.id}'
                run_at(command, at=starting_date)
            else:
                auction.start()

    @classmethod
    def start_auction_command(cls, id):
        auction = cls.get_auction(id)
        if auction:
            auction.start()

    @classmethod
    def bid_in_auction(cls, *, user_id, auction_id, amount):
        auction = cls.get_auction(auction_id)
        if auction:
            bid = Bid(amount=amount, user_id=user_id, auction=auction)
            return bid

    @classmethod
    def get_auction(cls, id):
        if not cls._auctions.get(id):
            # search in db
            pass
        else:
            return cls._auctions[id]


auction_manager = AuctionManager()

if __name__ == '__main__':
    command = 'python app/auction/start_auction.py 11'
    time = datetime.datetime.now() + datetime.timedelta(minutes=1)
    run_at(command=command, at=time)
