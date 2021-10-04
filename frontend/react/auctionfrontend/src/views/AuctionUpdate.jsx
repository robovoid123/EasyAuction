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
    const {token} = useContext(UserContext)

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
        const requestOptions = {
            method: 'PUT',
            headers: {
                "Content-Type": "application/json",
                Authorization: "bearer " + token[0],
            },
            body: JSON.stringify({
                name: name,
                description: description,
            }),
            mode: 'cors',
        }

        const response = await fetch(`/api/v1/products/${auction.product.id}`, requestOptions)
        const data = await response.json()

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

            const responseImage = await fetch(`api/v1/products/${data.id}/images`, requestOptionsForImage)
            const imageResponse = await responseImage.json()
        }


        const requestOptionsForUpdatingAuction = {
            method: 'PUT',
            headers: {
                "Content-Type": "application/json",
                Authorization: "bearer " + token[0],
            },
            body: JSON.stringify({
                "auction_in": {
                    "starting_amount": parseInt(startingAmount),
                    "bid_cap": parseInt(bidCap),
                    "reserve": parseInt(reserve),
                }
            }),
            mode: 'cors',
        }

        const responseUpdateAuction = await fetch(`/api/v1/auctions/${auction.id}`, requestOptionsForUpdatingAuction)
        const UpdateAuctionResponse = await responseUpdateAuction.json()

        if (!responseUpdateAuction.ok) {
            let responseErrorMessage = UpdateAuctionResponse.detail
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
        if (!name){
            setName(auction.product.name)
        }
        if (!description) {
            setDescription(auction.product.description)
        }
        if (!startingAmount) {
            setStartingAmount(auction.starting_amount)
        }
        if (!bidCap) {
            setBidCap(auction.bid_cap)
        }
        if (!reserve) {
            setReserve(auction.reserve)
        }
        submitProductUpdate()
    }

    return (
        <section className="vh-90">
            <div className="container mt-4">
                {isLoading ? <div>Loading..</div> : (
                <div className="row">
                    <div className="col-sm-6 text-black">
                        <div className="d-flex align-items-center h-custom-2 px-5 ms-xl-4 mt-5 pt-5 pt-xl-0 mt-xl-n5">
                            <form style={{ width: "23rem" }} onSubmit={handleSubmit}>
                                <h3 className="fw-normal mb-3 pb-3" style={{ letterSpacing: "1px" }}>Update Product</h3>

                                <div className="form-outline mb-4">
                                    <input type="text" className="form-control form-control-lg" placeholder={auction.product.name} value={name} onChange={(e) => setName(e.target.value)} />
                                </div>

                                <div className="form-outline mb-4">
                                    <input type="text" className="form-control form-control-lg" placeholder={auction.product.description} value={description} onChange={(e) => setDescription(e.target.value)} />
                                </div>

                                <div className="form-outline mb-4">
                                    <input type="text" className="form-control form-control-lg" placeholder={auction.starting_amount} value={startingAmount} onChange={(e) => setStartingAmount(e.target.value)} />
                                </div>

                                <div className="form-outline mb-4">
                                    <input type="text" className="form-control form-control-lg" placeholder={auction.bid_cap} value={bidCap} onChange={(e) => setBidCap(e.target.value)} />
                                </div>

                                <div className="form-outline mb-4">
                                    <input type="text" className="form-control form-control-lg" placeholder={auction.reserve} value={reserve} onChange={(e) => setReserve(e.target.value)} />
                                </div>

                                <div className="form-outline mb-4">
                                    <input type="file" className="form-control form-control-lg" onChange={(e) => setImage(e.target.files[0])} />
                                </div>

                                <ErrorMessage message={errorMessage} />

                                <div className="pt-1 mt-3 mb-4">
                                    <button className="btn btn-info btn-lg btn-block text-light" type="submit">Update Product</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>)}
            </div>
        </section>
    )
}