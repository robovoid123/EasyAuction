import React from 'react'
import { BidHandleButton } from '../components/BidHandleButton';

const ItemPage = props => {
    const [auction, setAuction] = React.useState([])
    const [bid, setBid] = React.useState("")
    const [isLoading, setIsLoading] = React.useState(true)

    var id = props.location.state

    React.useEffect(() => {
        fetch(`/api/v1/auctions/${id}`, { mode: 'cors' })
            .then((response) => response.json())
            .then((json) => {
                setAuction(json)
                setIsLoading(false)
            });
    }, [id]);



    return (
        <div className="container mt-5">
            {isLoading ? <div>Loading...</div> : (<div className="row">
                <div className="col-md-7">
                    <div className="row mb-5">
                        <div className="col-md-12">
                            <img src="https://dummyimage.com/700x500/000/fff" className="img-fluid " alt="dummy" />
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-md-12">
                            <h3 className="text-muted border-bottom border-secondary ">DESCRIPTION</h3>
                            <p>{auction.product.description}</p>
                        </div>
                    </div>
                </div>
                <div className="col-md-5">
                    <div className="row">
                        <div className="col-md-12 mt-2">
                            <h1>{auction.product.name}</h1>
                        </div>
                    </div>
                    <div className="row my-2">
                        <div className="col-md-12">
                            <span className="monospaced">Bid Cap {new Intl.NumberFormat("en-GB", { style: "currency", currency: "USD", maximumFractionDigits: 2 }).format(auction.bid_cap)}</span>
                            <span className="monospaced">Time Remaining</span>
                        </div>
                    </div>
                    <div className="row">
                        <div className="card p-4" style={{height:"20rem"}}>
                            <h2 className="mb-4">{new Intl.NumberFormat("en-GB", {style: "currency",currency: "USD",maximumFractionDigits: 2 }).format(auction.current_bid_amount)}</h2>

                            <label>YOUR MAXIMUM BID:</label>
                            <input type="text" className="form-control mb-3 mt-2" placeholder="Enter price to bid" value={bid} onChange={(e) => setBid(e.target.value)} required />
                            <BidHandleButton id={id} bid={bid} />
                        </div>
                    </div>
                </div>
            </div>)}

        </div>
    )
}

export default ItemPage