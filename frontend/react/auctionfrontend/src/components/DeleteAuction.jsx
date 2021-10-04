import React, {useContext, useState} from 'react'
import { ErrorMessage } from "./ErrorMessage";
import { UserContext } from "../context/UserContext";

export const DeleteAuction = ({id}) => {
    const [errorMessage, setErrorMessage] = useState("")
    const {token} = useContext(UserContext)

    const submitDeleteAuction = async () => {
        const requestOptions = {
            method: 'DELETE',
            headers: {
                "Content-Type": "application/json",
                Authorization: "bearer " + token[0],
            },
            mode: 'cors',
        }

        const response = await fetch(`/api/v1/auctions/${id}`, requestOptions)
        const data = await response.json()

        const requestOptionsProductDelete = {
            method: 'DELETE',
            headers: {
                "Content-Type": "application/json",
                Authorization: "bearer " + token[0],
            },
            mode: 'cors',
        }

        const responseDeleteProduct = await fetch(`/api/v1/products/${data.product_id}`, requestOptionsProductDelete)
        const dataDeleteProduct = await responseDeleteProduct.json()

        if (!response.ok) {
            let responseErrorMessage = dataDeleteProduct.detail
            // if error message from backend is a string then only set ErrorMessage
            // TODO: error message which are object need to be handled seperately
            if (typeof (responseErrorMessage) !== 'string') {
                responseErrorMessage = ''
            }
            setErrorMessage(responseErrorMessage)
        } else {
            window.location.reload(); 
        }
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        submitDeleteAuction()
    }

    return (
        <>
            <ErrorMessage message={errorMessage} />
            <button className="btn btn-info mx-2 my-2 text-light" onClick={handleSubmit}>Delete Product</button>
        </>
    )
}