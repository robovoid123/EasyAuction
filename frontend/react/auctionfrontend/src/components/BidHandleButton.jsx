import React, { useContext } from 'react'
import { UserContext } from '../context/UserContext'
import { ErrorMessage } from '../components/ErrorMessage'

export const BidHandleButton = ({id, bid}) => {
    const{token} = useContext(UserContext)
    const [errorMessage, setErrorMessage] = React.useState("")

    const submitBid = async () => {
        const requestOptions = {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
                Authorization: "bearer " + token[0],
            },
            body: JSON.stringify(
                bid
            ),
            mode: 'cors',
        }

        const response = await fetch(`/api/v1/auctions/${id}/bid`, requestOptions)
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
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        submitBid()
    }

    return (
        <>
            {token[0] === 'null' || !token[0] ? (
                <>
                    <button className="btn btn-info text-light fw-bold fs-5 mb-4" disabled>PLACE BID</button>
                    <p className="text-danger">Please login to bid or signup if account is not opened.</p>
                </>
            ) : (
                <>
                    <ErrorMessage message={errorMessage} />
                    <button className="btn btn-info text-light fw-bold fs-5 mb-4" onClick={handleSubmit}>PLACE BID</button>
                    <p className="text-muted">All bid place will be incremented bu $1.25.</p>
                </>
            )}
        </>
    )
}