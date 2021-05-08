from apscheduler.schedulers.background import BackgroundScheduler

from app.auction.redis import redis
from app.auction.auction import Auction
from app.auction.auction_strategy import AuctionType
from app.auction.bid import Bid


class AuctionManager:
    def __init__(self):

        self.sched = BackgroundScheduler()
        self.sched.start()

    def create_auction(self,
                       *,
                       product_id,
                       starting_bid_amount,
                       bid_cap=None,
                       reserve=None,
                       ending_date,
                       auction_type=AuctionType.ENGLISH):

        new_auction = Auction(
            product_id=product_id,
            starting_bid_amount=starting_bid_amount,
            bid_cap=bid_cap,
            reserve=reserve,
            ending_date=ending_date,
            auction_type=auction_type
        )
        db_obj = new_auction.store_in_db()
        new_auction.id = db_obj.id

        new_auction.store_in_redis()
        return new_auction.serialize()

    def start_auction(self, id, starting_date=None):
        if starting_date:
            self.sched.add_job(lambda: self._start_auction(id),
                               'date', run_date=starting_date)
        else:
            self._start_auction(id)

    def _start_auction(self, id):
        auction = self.get_auction(id)
        if auction:
            auction.start()
            print('--------Auction started--------')

    def bid_in_auction(self, *, user_id, auction_id, amount):
        auction = self.get_auction(auction_id)
        if auction:
            bid = Bid(amount=amount, user_id=user_id, auction=auction)
            return bid

    def get_auction(self, id):
        auction = redis.get(f'auction_{id}')
        if auction:
            return Auction.load_from_dict(auction)
        else:
            pass


auction_manager = AuctionManager()
