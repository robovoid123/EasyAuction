import ProductIndiButton from "../components/ProductIndiButton"
import React, { useState } from "react"

const SearchResult = props => {

    const [auctions, setAuctions] = React.useState([])
    const [isLoading, setIsLoading] = useState(true)

    var searchKey = props.location.state

    React.useEffect(() => {
        fetch(`/api/v1/auctions/?skip=0&limit=80&like=${searchKey}`, { mode: 'cors' })
            .then((response) => response.json())
            .then((json) => {
                setAuctions(json)
                setIsLoading(false)
            });
    }, [searchKey]);

    return (
        <div className="container mt-5">
            <h2>Your Search Results</h2>
            {isLoading ? <div className="spinner-border text-info" role="status"></div>: (
                <div className="row g-4">
                    {auctions.map((auction) => {
                        if (auction.state === 'ongoing') {
                            return (
                                <div className="col-12 col-md-4 col-lg-3 custom-card" key={auction.id}>
                                    <div className="card">
                                        <img src={(auction.product.images.length) >= 1 ? "http://localhost:8000" + auction.product.images[auction.product.images.length - 1].url : "https://dummyimage.com/300x200/000/fff"} className="card-img-top " alt="..." />
                                        <div className="card-body border-top">
                                            <h5 className="card-title">{auction.product.name}</h5>
                                            <p className="card-text"><span>Current Bid: </span>{new Intl.NumberFormat("en-GB", { style: "currency", currency: "USD", maximumFractionDigits: 2 }).format(auction.current_bid_amount)}</p>
                                            <p className="card-text"><span>Ending Date: </span>{new Intl.DateTimeFormat("en-GB").format(new Date(auction.ending_date))}</p>
                                            <ProductIndiButton id={auction.id} />
                                        </div>
                                    </div>
                                </div>
                            )
                        } else {
                            return <></>
                        }
                    })}
                </div>
            )}
        </div>
    )
}

export default SearchResult