import React, { useEffect, useState, useContext } from 'react'
import { ErrorMessage } from '../components/ErrorMessage'
import { UserContext } from "../context/UserContext";
import { Redirect } from 'react-router-dom';

export const ProductUpdate = props => {
    const [ product, setProduct] = useState([])
    const [name, setName] = useState("")
    const [description, setDescription] = useState("")
    const [errorMessage, setErrorMessage] = useState("")
    const [token,] = useContext(UserContext)

    var id = props.location.state

    useEffect(() => {
        fetch(`/api/v1/products/${id}`, {mode: 'cors'})
        .then((response) => response.json())
        .then((json) => {
            setProduct(json)
        })
    }, [id])

    const submitProductUpdate = async () => {
        const requestOptions = {
            method: 'PUT',
            headers: {
                "Content-Type": "application/json",
                Authorization: "bearer " + token,
            },
            body: JSON.stringify({
                product_in: {
                    name: name,
                    description: description,
                },
            }),
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
        } else{
            return <Redirect to="product"></Redirect>
        }
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        submitProductUpdate()
    }

    return (
        <section className="vh-90">
            <div className="container mt-4">
                <div className="row">
                    <div className="col-sm-6 text-black">
                        <div className="d-flex align-items-center h-custom-2 px-5 ms-xl-4 mt-5 pt-5 pt-xl-0 mt-xl-n5">
                            <form style={{ width: "23rem" }} onSubmit={handleSubmit}>
                                <h3 className="fw-normal mb-3 pb-3" style={{ letterSpacing: "1px" }}>Update Product</h3>

                                <div className="form-outline mb-4">
                                    <input type="text" className="form-control form-control-lg" placeholder={product.name} value={name} onChange={(e) => setName(e.target.value)} />
                                </div>

                                <div className="form-outline mb-4">
                                    <input type="text" className="form-control form-control-lg" placeholder={product.description} value={description} onChange={(e) => setDescription(e.target.value)}/>
                                </div>

                                <ErrorMessage message={errorMessage} />

                                <div className="pt-1 mt-3 mb-4">
                                    <button className="btn btn-info btn-lg btn-block text-light" type="submit">Update Product</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}
