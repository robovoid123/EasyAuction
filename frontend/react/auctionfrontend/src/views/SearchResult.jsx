import ProductIndiButton from "../components/ProductIndiButton"
import React from "react"

const SearchResult = props => {

    const [auctions, setAuctions] = React.useState([])

    var searchKey = props.location.state

    console.log(searchKey)

    React.useEffect(() => {
        fetch(`/api/v1/auctions/?skip=0&limit=80&like=${searchKey}`, {mode: 'cors'})
            .then((response) => response.json()) 
            .then((json) => {
                console.log(json)
                setAuctions(json)
            });
    }, [searchKey]);

    return (
        <div className="container mt-5">
           <h2>Your Search Results</h2>
            <div className="row g-4">
                {auctions.map((auction) => (
                    <div className="col-12 col-md-4 col-lg-3">
                        <div className="card">
                            <img src="https://dummyimage.com/300x200/000/fff" className="card-img-top" alt="..." />
                            <div className="card-body">
                                <h5 className="card-title">{auction.product.name}</h5>
                                <p className="card-text">{auction.product.description}</p>
                                <p className="card-text"><span>Current Bid Amount: </span>${auction.current_bid_amount}</p>
                                <p className="card-text"><span>Ending Date: </span>{auction.ending_date}</p>
                                <ProductIndiButton id={auction.id} />
                            </div>
                        </div>
                    </div>
                ))}
            </div> 
        </div>
    )
}

export default SearchResult