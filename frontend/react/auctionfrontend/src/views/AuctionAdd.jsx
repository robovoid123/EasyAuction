import React, { useState, useContext } from "react";
import { ErrorMessage } from "../components/ErrorMessage";
import { UserContext } from "../context/UserContext";

const AuctionAdd = props => {
    const [name, setName] = useState("")
    const [description, setDescription] = useState("")
    const [startingAmount, setStartingAmount] = useState("")
    const [bidCap, setBidCap] = useState("")
    const [reserve, setReserve] = useState("")
    const [image, setImage] = useState(null)
    const [errorMessage, setErrorMessage] = useState("")
    const {token} = useContext(UserContext)

    const submitProductAdd = async () => {
        const requestOptions = {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
                Authorization: "bearer " + token[0],
            },
            body: JSON.stringify({
                product_in: {
                    name: name,
                    description: description
                },
                categories: [
                    "a"
                ]
            }),
            mode: 'cors',
        }

        const response = await fetch("/api/v1/products", requestOptions)
        const data = await response.json()

        if (!response.ok) {
            let responseErrorMessage = data.detail
            // if error message from backend is a string then only set ErrorMessage
            // TODO: error message which are object need to be handled seperately
            if (typeof (responseErrorMessage) !== 'string') {
                responseErrorMessage = ''
            }
            setErrorMessage(responseErrorMessage)
        } 

        // uploading image
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

        const responseImage = await fetch(`/api/v1/products/${data.id}/images`, requestOptionsForImage)
        const imageResponse = await responseImage.json()

        if (!response.ok) {
            let responseErrorMessage = imageResponse.detail
            // if error message from backend is a string then only set ErrorMessage
            // TODO: error message which are object need to be handled seperately
            if (typeof (responseErrorMessage) !== 'string') {
                responseErrorMessage = ''
            }
            setErrorMessage(responseErrorMessage)
        } 

        // Creating Auction
        const requestOptionsForCreatingAuction = {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
                Authorization: "bearer " + token[0],
            },
            body: JSON.stringify({
                "starting_amount": parseInt(startingAmount),
                "bid_cap": parseInt(bidCap),
                "reserve": parseInt(reserve),
                "product_id": data.id,
            }),
            mode: 'cors',
        }

        const responseCreateAuction = await fetch("/api/v1/auctions", requestOptionsForCreatingAuction)
        const createAuctionResponse = await responseCreateAuction.json()

        if (!response.ok) {
            let responseErrorMessage = createAuctionResponse.detail
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
        submitProductAdd()
    }

    return (
        <section className="vh-90">
            <div className="container mt-4">
                <div className="row">
                    <div className="col-sm-6 text-black">
                        <div className="d-flex align-items-center h-custom-2 px-5 ms-xl-4 mt-5 pt-5 pt-xl-0 mt-xl-n5">
                            <form style={{ width: "23rem" }} onSubmit={handleSubmit}>
                                <h3 className="fw-normal mb-3 pb-3" style={{ letterSpacing: "1px" }}>Add Product</h3>

                                <div className="form-outline mb-4">
                                    <input type="text" className="form-control form-control-lg" placeholder="Product Name" value={name} onChange={(e) => setName(e.target.value)} required />
                                </div>

                                <div className="form-outline mb-4">
                                    <input type="text" className="form-control form-control-lg" placeholder="Product Description" value={description} onChange={(e) => setDescription(e.target.value)} required />
                                </div>

                                <div className="form-outline mb-4">
                                    <input type="text" className="form-control form-control-lg" placeholder="Starting Amount" value={startingAmount} onChange={(e) => setStartingAmount(e.target.value)} required />
                                </div>
                                <div className="form-outline mb-4">
                                    <input type="text" className="form-control form-control-lg" placeholder="Bid Cap" value={bidCap} onChange={(e) => setBidCap(e.target.value)} required />
                                </div>

                                <div className="form-outline mb-4">
                                    <input type="text" className="form-control form-control-lg" placeholder="Reserve" value={reserve} onChange={(e) => setReserve(e.target.value)} required />
                                </div>

                                <div className="form-outline mb-4">
                                    <input type="file" className="form-control form-control-lg" onChange={(e) => setImage(e.target.files[0])} />
                                </div>

                                <ErrorMessage message={errorMessage} />

                                <div className="pt-1 mt-3 mb-4">
                                    <button className="btn btn-info btn-lg btn-block text-light" type="submit">Create Product</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default AuctionAdd