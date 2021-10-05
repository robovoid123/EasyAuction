import ProductIndiButton from "./ProductIndiButton"
import React from "react"

const FeaturedList = () => {

    const [auctions, setAuctions] = React.useState([])

    React.useEffect(() => {
        fetch("/api/v1/auctions/?skip=0&limit=5&states=ongoing&order_by=bid_count", { mode: 'cors' })
            .then((response) => response.json())
            .then((json) => {
                setAuctions(json)
            });
    }, []);

    return (
        <div className="container mt-5">
            <h2>Featured Auctions</h2>
            <div className="row g-4">
                {auctions.map((auction) => {
                    if (auction.state === 'ongoing') {
                        return (
                            <div className="col-12 col-md-4 col-lg-3" key={auction.id}>
                                <div className="card">
                                    <img src={(auction.product.images.length) >= 1 ? "http://localhost:8000" + auction.product.images[auction.product.images.length - 1].url : "https://dummyimage.com/300x200/000/fff"} className="card-img-top" alt="..." />
                                    <div className="card-body">
                                        <h5 className="card-title">{auction.product.name}</h5>
                                        <p className="card-text"><span>Current Bid Amount: </span>{new Intl.NumberFormat("en-GB", { style: "currency", currency: "USD", maximumFractionDigits: 2 }).format(auction.current_bid_amount)}</p>
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
        </div>
    )
}

export default FeaturedList
