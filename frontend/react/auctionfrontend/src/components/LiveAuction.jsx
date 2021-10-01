import ProductIndiButton from "./ProductIndiButton"
import React from "react";

const LiveAuction = () => {
    
    const [auctions, setAuctions] = React.useState([])

    React.useEffect(() => {
        fetch("/api/v1/auctions/", {mode: 'cors'})
            .then((response) => response.json()) 
            .then((json) => {
                console.log(json)
                setAuctions(json)
            });
    }, []);

    return (
        <div className="container mt-5">
           <h2>Live Auctions</h2>
            <div class="row g-4">
               {auctions.map((auction) => (
                    <div className="col-12 col-md-4 col-lg-3">
                        <div className="card">
                            <img src="https://dummyimage.com/300x200/000/fff" className="card-img-top" alt="..." />
                            <div className="card-body">
                                <h5 className="card-title">{auction.product.name}</h5>
                                <p className="card-text">{auction.product.description}</p>
                                <p className="card-text"><span>Current Bid Amount: </span>${auction.current_bid_amount}</p>
                                <p className="card-text"><span>Ending Date: </span>{auction.ending_date}</p>
                                <ProductIndiButton productid={auction.id} />
                            </div>
                        </div>
                    </div>
               ))} 
            </div>
        </div>
    )
}

export default LiveAuction
