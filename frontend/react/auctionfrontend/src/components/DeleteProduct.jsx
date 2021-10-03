import React, {useContext, useState} from 'react'
import { ErrorMessage } from "../components/ErrorMessage";
import { UserContext } from "../context/UserContext";

export const DeleteProduct = ({id}) => {
    const [errorMessage, setErrorMessage] = useState("")
    const {token} = useContext(UserContext)

    const submitProductAdd = async () => {
        const requestOptions = {
            method: 'DELETE',
            headers: {
                "Content-Type": "application/json",
                Authorization: "bearer " + token[0],
            },
            mode: 'cors',
        }

        const response = await fetch(`/api/v1/products/${id}`, requestOptions)
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
        submitProductAdd()
    }

    return (
        <>
            <ErrorMessage message={errorMessage} />
            <button className="btn btn-info mx-2 my-2 text-light" onClick={handleSubmit}>Delete Product</button>
        </>
    )
}
