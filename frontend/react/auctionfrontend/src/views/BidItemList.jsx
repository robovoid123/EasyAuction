import ProductIndiButton from "../components/ProductIndiButton"
import React, { useContext, useState } from "react"
import { UserContext } from "../context/UserContext"

const FeaturedList = () => {
    const { userData } = useContext(UserContext)
    const [auctions, setAuctions] = React.useState([])
    const [isLoading, setIsLoading] = useState(true)

    React.useEffect(() => {
        fetch(`/api/v1/bids/${userData[0]}/auctions?skip=0&limit=100`, { mode: 'cors' })
            .then((response) => response.json())
            .then((json) => {
                setAuctions(json)
                setIsLoading(false)
            });
    }, [userData]);

    // console.log(auctions, "top")

    return (
        <div className="container mt-5">
            <h2>List of item bid on</h2>
            {isLoading ? <div>Loading..</div> : (
                <div className="row g-4">
                    {auctions.map((auction) => {
                        {auction.map((inside) => {
                        return (
                            <div className="col-12 col-md-4 col-lg-3" key={inside.id}>
                                <div className="card">
                                    {console.log(inside, "-----")}
                                    <img src={(inside.product.images.length) >= 1 ? "http://localhost:8000" + inside.product.images[inside.product.images.length - 1].url : "https://dummyimage.com/300x200/000/fff"} className="card-img-top" alt="..." />
                                    <div className="card-body">
                                        <h5 className="card-title">{inside.product.name}</h5>
                                        <p className="card-text"><span>Current Bid Amount: </span>{new Intl.NumberFormat("en-GB", { style: "currency", currency: "USD", maximumFractionDigits: 2 }).format(inside.current_bid_amount)}</p>
                                        <p className="card-text"><span>Ending Date: </span>{new Intl.DateTimeFormat("en-GB").format(new Date(inside.ending_date))}</p>
                                        <ProductIndiButton id={inside.id} />
                                    </div>
                                </div>
                            </div>
                        )})}
                    }
                    )}
                </div>
            )}
        </div>
    )
}

export default FeaturedList

