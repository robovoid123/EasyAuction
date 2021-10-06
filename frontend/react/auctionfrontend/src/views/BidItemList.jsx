import ProductIndiButton from "../components/ProductIndiButton"
import React, { useContext, useState } from "react"
import { UserContext } from "../context/UserContext"

const FeaturedList = () => {
    const { userData } = useContext(UserContext)
    const [auctions, setAuctions] = React.useState([])
    const [isLoading, setIsLoading] = useState(true)
    const [sender, setSender] = useState()

    React.useEffect(() => {
        fetch(`/api/v1/bids/${userData[0]}/auctions?skip=0&limit=100`, { mode: 'cors' })
            .then((response) => response.json())
            .then((json) => {
                setAuctions(json)
                setIsLoading(false)
            });
    }, [userData]);

    const submitContact = async () => {
        const requestOptions = {
            method: 'GET',
            headers: {
                "Content-Type": "application/json",
            },
            mode: 'cors',
        }

        const response = await fetch(`/api/v1/users/${userData[0]}`, requestOptions)
        const data = await response.json()

        if (response.ok) {
            setSender(data)
        }
    }

    return (
        <div className="container mt-5">
            <h2>List of item bid on</h2>
            {isLoading ? <div className="spinner-border text-info" role="status"></div>: (
                <div className="row g-4">
                    {auctions.map((auction) => {
                        return (
                            <div className="col-12 col-md-4 col-lg-3" key={auction.id}>
                                <div className="card">
                                    <img src={(auction.product.images.length) >= 1 ? "http://localhost:8000" + auction.product.images[auction.product.images.length - 1].url : "https://dummyimage.com/300x200/000/fff"} className="card-img-top" alt="..." />
                                    <div className="card-body">
                                        <h5 className="card-title">{auction.product.name}</h5>
                                        <p className="card-text"><span>Current Bid: </span>{new Intl.NumberFormat("en-GB", { style: "currency", currency: "USD", maximumFractionDigits: 2 }).format(auction.current_bid_amount)}</p>
                                        <p className="card-text"><span>Ending Date: </span>{new Intl.DateTimeFormat("en-GB").format(new Date(auction.ending_date))}</p>
                                        {auction.state === 'ended' ? <span className="badge rounded-pill bg-info text-light">Auction Ended</span> :
                                            <ProductIndiButton id={auction.id} />
                                        }
                                        {console.log(typeof auction.final_winner_id,typeof parseInt(userData[0]))}
                                        {auction.final_winner_id === parseInt(userData[0]) ? 
                                        <>
                                        <button type="button" class="btn btn-info ms-3 text-light" data-bs-toggle="modal" data-bs-target="#staticBackdrop" onClick={submitContact}>
                                        Contact Buyer
                                        </button>

                                        <div class="modal fade" id="staticBackdrop" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
                                        <div class="modal-dialog">
                                            <div class="modal-content">
                                            <div class="modal-header">
                                                <h5 class="modal-title" id="staticBackdropLabel">Buyers Info</h5>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body">
                                                {sender ? 
                                                    <p>{sender.email}</p>:<></>
                                                }
                                            </div>
                                            <div class="modal-footer">
                                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                            </div>
                                            </div>
                                        </div>
                                        </div>
                                        </>

                                        : <></>}
                                    </div>
                                </div>
                            </div>
                        )
                    }
                    )}
                </div>
            )}
        </div>
    )
}

export default FeaturedList