import React, {useContext} from 'react'
import { BidHandleButton } from '../components/BidHandleButton';
import { UserContext } from "../context/UserContext";

const ItemPage = props => {
    const [auction, setAuction] = React.useState([])
    const [bid, setBid] = React.useState("")
    const [isLoading, setIsLoading] = React.useState(true)
    const { token } = useContext(UserContext)

    var id = props.location.state

    React.useEffect(() => {
        fetch(`/api/v1/auctions/${id}`, { mode: 'cors' })
            .then((response) => response.json())
            .then((json) => {
                setAuction(json)
                setIsLoading(false)
            });
    }, [id]);

    const handleBidItNow = (id) =>{
        console.log(id, "---------------");
        const submitBitItNow = async () => {
            const requestOptions = {
                method: 'POST',
                headers: {
                    Authorization: "bearer " + token[0],
                },
                mode: 'cors',
            }
            const response = await fetch(`/api/v1/auctions/${id}/buy_it_now`, requestOptions)
            const data = await response.json()
            
            if (response.ok) {
                window.location.reload()
            }
        }
        submitBitItNow()
    }

    return (
        <div className="container mt-5">
            {isLoading ? <div className="spinner-border text-info" role="status"></div>: (<div className="row">
                <div className="col-md-7">
                    <div className="row mb-5">
                        <div className="col-md-12">
                            <img src={(auction.product.images.length) >= 1 ? "http://localhost:8000" + auction.product.images[auction.product.images.length - 1].url : "https://dummyimage.com/600x400/000/fff"} alt="Product Display" className="img-fluid" />
                            {/* <img src="https://dummyimage.com/700x500/000/fff" className="img-fluid " alt="dummy" /> */}
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
                            <button className="btn btn-info text-light ms-4" onClick={() => handleBidItNow(auction.id)}>Bid It Now</button>
                        </div>
                    </div>
                    <div className="row">
                        <div className="card p-4" style={{ height: "20rem" }}>
                            <h2 className="mb-4">{new Intl.NumberFormat("en-GB", { style: "currency", currency: "USD", maximumFractionDigits: 2 }).format(auction.current_bid_amount)}</h2>

                            <label>YOUR MAXIMUM BID:</label>
                            <input type="text" className="form-control mb-3 mt-2" placeholder="Enter price to bid" value={bid} onChange={(e) => setBid(e.target.value.replace(/\D/g, ""))} required />
                            <BidHandleButton id={id} bid={bid} />
                        </div>
                    </div>
                </div>
            </div>)}

        </div>
    )
}

export default ItemPage