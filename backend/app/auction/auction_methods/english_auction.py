from fastapi import HTTPException, status


class EnglishAuction:

    INC_AMT = 1.25

    def __call__(self, db, auction, auction_session, bid):

        current_highest_bid = auction_session.current_highest_bid

        if not current_highest_bid:

            if bid.amount > auction.starting_bid_amount:

                auction_session.current_highest_bid_id = bid.id
                auction_session.bid_line = bid.amount + EnglishAuction.INC_AMT

            else:

                sb = auction.starting_bid_amount

                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail=f'bid amount should be greater than {sb}'
                )

        elif bid.amount > auction_session.bid_line:

            auction_session.current_highest_bid_id = bid.id
            auction_session.bid_line = bid.amount + EnglishAuction.INC_AMT

        else:

            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f'bid amount should be greater than {auction_session.bid_line}'
            )

        return auction, auction_session
