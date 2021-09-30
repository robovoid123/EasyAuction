import React from 'react';


const AuctionShowCase = ({ auctions }) => (
    <section>
        <div className="container">
            <div className="row text-center">
                <h4 className="fw-bold lead heading">Auction Showcase</h4>
                <div className="heading-line mb-3"></div>
            </div>
        </div>
        <div className="container">
            <div className="auction-items">
                <div className="row g-4">
                    {auctions.map((auction) => (
                        <div className="col-12 col-md-4 col-lg-3 auction-item" key={auction.id}>
                            <div className="card">
                                <img src="https://dummyimage.com/300x200/000/fff" className="card-img-top" alt="..." />
                                <div className="card-body">
                                    <h5 className="card-title">{auction.product.name}</h5>
                                    <p className="card-text">{auction.product.description}</p>
                                    <p className="card-text"><span>Current Bid Amount: </span>${auction.current_bid_amount}</p>
                                    <p className="card-text"><span>Ending Date: </span>{auction.ending_date}</p>
                                    <a href="#" className="btn btn-primary">BID Now</a>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    </section>
)

export default AuctionShowCase;