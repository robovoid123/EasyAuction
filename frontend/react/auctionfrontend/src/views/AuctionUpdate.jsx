import React, { useEffect, useState, useContext } from 'react'
import { ErrorMessage } from '../components/ErrorMessage'
import { UserContext } from "../context/UserContext";

export const AuctionUpdate = props => {
    const [auction, setAuction] = useState([])
    const [name, setName] = useState()
    const [description, setDescription] = useState()
    const [startingAmount, setStartingAmount] = useState()
    const [bidCap, setBidCap] = useState()
    const [reserve, setReserve] = useState()
    const [isLoading, setIsLoading] = React.useState(true)
    const [image, setImage] = useState(null)
    const [errorMessage, setErrorMessage] = useState("")
    const { token } = useContext(UserContext)

    var id = props.location.state

    useEffect(() => {
        fetch(`/api/v1/auctions/${id}`, { mode: 'cors' })
            .then((response) => response.json())
            .then((json) => {
                setAuction(json)
                setIsLoading(false)
            })
    }, [id])


    const submitProductUpdate = async () => {
        let productBody = {}
        if (name) {
            productBody.name = name
        }
        if (description) {
            productBody.description = description
        }

        const requestOptionsForProduct = {
            method: 'PUT',
            headers: {
                "Content-Type": "application/json",
                Authorization: "bearer " + token[0],
            },
            body: JSON.stringify(productBody),
            mode: 'cors',
        }

        const responseProduct = await fetch(`/api/v1/products/${auction.product.id}`, requestOptionsForProduct)
        const productResponse = await responseProduct.json()
        // TODO: check if productResponse ok

        // uploading image
        if (image) {
            const imageData = new FormData()
            imageData.append('image', image)

            const requestOptionsForImage = {
                method: 'POST',
                headers: {
                    Authorization: "bearer " + token[0],
                },
                body: imageData,
                mode: 'cors',
            }

            const responseImage = await fetch(`api/v1/products/${productResponse.id}/images`, requestOptionsForImage)
            const imageResponse = await responseImage.json()
            // TODO: check if image response ok
        }

        let auctionBody = {}
        if (startingAmount) {
            auctionBody.starting_amount = startingAmount
        }
        if (bidCap) {
            auctionBody.bid_cap = bidCap
        }
        if (reserve) {
            auctionBody.reserve = reserve
        }

        const requestOptionsForAuction = {
            method: 'PUT',
            headers: {
                "Content-Type": "application/json",
                Authorization: "bearer " + token[0],
            },
            body: JSON.stringify({
                "auction_in": auctionBody
                // TODO: ending_date update
            }),
            mode: 'cors',
        }

        const responseUpdateAuction = await fetch(`/api/v1/auctions/${auction.id}`, requestOptionsForAuction)
        const auctionResponse = await responseUpdateAuction.json()

        if (!responseUpdateAuction.ok) {
            let responseErrorMessage = auctionResponse.detail
            // if error message from backend is a string then only set ErrorMessage
            // TODO: error message which are object need to be handled seperately
            if (typeof (responseErrorMessage) !== 'string') {
                responseErrorMessage = ''
            }
            setErrorMessage(responseErrorMessage)
        } else {
            props.history.push('product')
        }
    }



    const handleSubmit = (e) => {
        e.preventDefault()
        submitProductUpdate()
    }

    return (
        <section className="vh-90">
            <div className="container mt-4">
                {isLoading ? <div>Loading..</div> : (
<<<<<<< HEAD
                <div className="row">
                    <div className="col-sm-6 text-black">
                        <div className="d-flex align-items-center h-custom-2 px-5 ms-xl-4 mt-5 pt-5 pt-xl-0 mt-xl-n5">
                            <form style={{ width: "23rem" }} onSubmit={handleSubmit}>
                                <h3 className="fw-normal mb-3 pb-3" style={{ letterSpacing: "1px" }}>Update Product</h3>

                                <div className="form-outline mb-4">
                                    <label for="exampleInputPassword1" class="form-label">Product Name</label>
                                    <input type="text" className="form-control form-control-lg" placeholder={auction.product.name} value={name} onChange={(e) => setName(e.target.value)} />
                                </div>

                                <div className="form-outline mb-4">
                                    <label for="exampleInputPassword1" class="form-label">Description</label>
                                    <input type="text" className="form-control form-control-lg" placeholder={auction.product.description} value={description} onChange={(e) => setDescription(e.target.value)} />
                                </div>

                                <div className="form-outline mb-4">
                                    <label for="exampleInputPassword1" class="form-label">Starting Amount</label>
                                    <input type="text" className="form-control form-control-lg" placeholder={auction.starting_amount} value={startingAmount} onChange={(e) => setStartingAmount(e.target.value)} />
                                </div>

                                <div className="form-outline mb-4">
                                    <label for="exampleInputPassword1" class="form-label">Bid Cap</label>
                                    <input type="text" className="form-control form-control-lg" placeholder={auction.bid_cap} value={bidCap} onChange={(e) => setBidCap(e.target.value)} />
                                </div>

                                <div className="form-outline mb-4">
                                    <label for="exampleInputPassword1" class="form-label">Reserve</label>
                                    <input type="text" className="form-control form-control-lg" placeholder={auction.reserve} value={reserve} onChange={(e) => setReserve(e.target.value)} />
                                </div>

                                <div className="form-outline mb-4">
                                    <label for="exampleInputPassword1" class="form-label">Add Image</label>
                                    <input type="file" className="form-control form-control-lg" onChange={(e) => setImage(e.target.files[0])} />
                                </div>

                                <ErrorMessage message={errorMessage} />

                                <div className="pt-1 mt-3 mb-4">
                                    <button className="btn btn-info btn-lg btn-block text-light" type="submit">Update Product</button>
                                </div>
                            </form>
=======
                    <div className="row">
                        <div className="col-sm-6 text-black">
                            <div className="d-flex align-items-center h-custom-2 px-5 ms-xl-4 mt-5 pt-5 pt-xl-0 mt-xl-n5">
                                <form style={{ width: "23rem" }} onSubmit={handleSubmit}>
                                    <h3 className="fw-normal mb-3 pb-3" style={{ letterSpacing: "1px" }}>Update Product</h3>

                                    <div className="form-outline mb-4">
                                        <label for="updateProductName" class="form-label">Name</label>
                                        <input type="text" id="updateProductName" className="form-control form-control-lg" placeholder={auction.product.name} value={name} onChange={(e) => setName(e.target.value)} />
                                    </div>

                                    <div className="form-outline mb-4">
                                        <label for="updateProductDescription" class="form-label">Description</label>
                                        <input type="text" id="updateProductDescription" className="form-control form-control-lg" placeholder={auction.product.description} value={description} onChange={(e) => setDescription(e.target.value)} />
                                    </div>

                                    <div className="form-outline mb-4">
                                        <label for="updateStartingAmount" class="form-label">Starting Bid Amount</label>
                                        <input type="text" id="updateStartingAmount" className="form-control form-control-lg" placeholder={auction.starting_amount} value={startingAmount} onChange={(e) => setStartingAmount(e.target.value)} />
                                    </div>

                                    <div className="form-outline mb-4">
                                        <label for="updateBidCap" class="form-label">Bid Cap</label>
                                        <input type="text" id="updateBidCap" className="form-control form-control-lg" placeholder={auction.bid_cap} value={bidCap} onChange={(e) => setBidCap(e.target.value)} />
                                    </div>

                                    <div className="form-outline mb-4">
                                        <label for="updateReserve" class="form-label">Reserve</label>
                                        <input type="text" id="updateReserve" className="form-control form-control-lg" placeholder={auction.reserve} value={reserve} onChange={(e) => setReserve(e.target.value)} />
                                    </div>

                                    <div className="form-outline mb-4">
                                        <label for="updateProductImage" class="form-label">Image</label>
                                        <input type="file" id="updateProductImage" className="form-control form-control-lg" onChange={(e) => setImage(e.target.files[0])} />
                                    </div>

                                    <ErrorMessage message={errorMessage} />

                                    <div className="pt-1 mt-3 mb-4">
                                        <button className="btn btn-info btn-lg btn-block text-light" type="submit">Update Product</button>
                                    </div>
                                </form>
                            </div>
                        </div>
                        <div className="col-sm-6 my-5">
                            <div className="container">
                                <img src={(auction.product.images.length) >= 1 ? "http://localhost:8000" + auction.product.images[auction.product.images.length - 1].url : "https://dummyimage.com/300x200/000/fff"} alt="Product Display" className="img-fluid" />
                            </div>
>>>>>>> 475b0a7ecb405813d24cc976cca42c7c9b9c73f8
                        </div>
                    </div>)}
            </div>
        </section>
    )
}