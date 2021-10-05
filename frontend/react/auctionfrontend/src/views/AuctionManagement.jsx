import React, { useContext, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { DeleteAuction } from '../components/DeleteAuction'
import { StartAuction } from '../components/StartAuction'
import { UserContext } from '../context/UserContext'

const Product = props => {
    const [auctions, setAuctions] = useState([])
    const { userData } = useContext(UserContext)

    // const userId = props.location.state

    useEffect(() => {
        fetch(`/api/v1/auctions/users/${userData[0]}?skip=0&limit=100&states=ongoing%2Cended%2Ccreated&order_by=last_bid_at`, { mode: 'cors' })
            .then((response) => response.json())
            .then((json) => {
                setAuctions(json)
            })
    }, [userData])


    return (
        <div className="container">
            <h1 className="my-3 border-bottom border-3">Auction Management</h1>
            <a href="productAdd" className="btn btn-info mb-4 text-light">Add Auction</a>
            {auctions.map((auction) => (
                <div className="card mb-3" key={auction.product.id}>
                    <div className="row g-0">
                        <div className="col-md-8 d-flex align-items-center px-4">
                            <div className="card-body">
                                <span className="badge rounded-pill bg-info text-light mb-2">{auction.state}</span>
                                <h3 className="mt-0 font-weight-bold mb-2 card-title">{auction.product.name}</h3>
                                <p className="font-italic text-muted mb-0 small card-text">{auction.product.description}</p>
                                <h4 className="font-weight-bold my-2 card-text">{new Intl.NumberFormat("en-GB", { style: "currency", currency: "USD", maximumFractionDigits: 2 }).format(auction.current_bid_amount ? auction.current_bid_amount : auction.starting_amount)}</h4>
                                <div className="d-flex">
                                    <Link to={{
                                        pathname: 'productUpdate',
                                        state: auction.id,
                                    }}>
                                        <button className="btn btn-info me-2 my-2 text-light">Update Product</button>
                                    </Link>
                                    <DeleteAuction id={auction.id} />
                                    {auction.state === 'ongoing' || auction.state === 'ended' ? <> </> : (
                                        <StartAuction id={auction.id} />
                                    )}
                                </div>
                            </div>
                        </div>
                        <div className="col-md-4 d-flex justify-content-center px-2 py-3">
                            <img src={(auction.product.images.length) >= 1 ? "http://localhost:8000" + auction.product.images[auction.product.images.length - 1].url : "https://dummyimage.com/300x200/000/fff"} alt="Product Display" width="400" className="img-fluid" />
                        </div>
                    </div>
                </div>
            ))}
        </div>
    )
}

export default Product
