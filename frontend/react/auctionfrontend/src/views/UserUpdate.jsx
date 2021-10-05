import React, { useEffect, useState, useContext } from 'react'
import { ErrorMessage } from '../components/ErrorMessage'
import { UserContext } from "../context/UserContext";
import { Link } from 'react-router-dom';

export const UserUpdate = () => {
    const [userData, setUserData] = useState()
    const [fullname, setFullName] = useState()
    const [password, setPassword] = useState()
    const [email, setEmail] = useState()
    const [isLoading, setIsLoading] = React.useState(true)
    const [image, setImage] = useState(null)
    const [errorMessage, setErrorMessage] = useState("")
    const { token } = useContext(UserContext)

    const requestUserMe = {
        method: 'GET',
        headers: {
            "Content-Type": "application/json",
            Authorization: "bearer " + token[0],
        },
        mode: 'cors',
    }

    React.useEffect(() => {
        fetch(`/api/v1/users/me`, requestUserMe)
            .then((response) => response.json())
            .then((json) => {
                setUserData(json)
                setIsLoading(false)
            });
    }, []);

    const submitUserUpdate = async () => {
        let productBody = {}
        if (fullname) {
            productBody.full_name = fullname
        }
        if (password) {
            productBody.password = password
        }
        if (email) {
            productBody.email = email
        }

        const requestOptions = {
            method: 'PUT',
            headers: {
                "Content-Type": "application/json",
                Authorization: "bearer " + token[0],
            },
            body: JSON.stringify(productBody),
            mode: 'cors',
        }

        const responseUser = await fetch(`/api/v1/users/me`, requestOptions)
        const userResponse = await responseUser.json()
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
            const responseImage = await fetch(`/api/v1/users/me/profile-pic`, requestOptionsForImage)
            const imageResponse = await responseImage.json()
            // TODO: check if image response ok
        }

        if (!responseUser.ok) {
            let responseErrorMessage = userResponse.detail
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
        submitUserUpdate()
    }

    return (
        <section className="vh-90">
            <div className="container mt-4">
                {isLoading ? <div>Loading..</div> : (
                    <div className="row">
                        <div className="col-sm-6 text-black">
                            <div className="d-flex align-items-center h-custom-2 px-5 ms-xl-4 mt-5 pt-5 pt-xl-0 mt-xl-n5">
                                <form style={{ width: "23rem" }} onSubmit={handleSubmit}>
                                    <h3 className="fw-normal mb-3 pb-3" style={{ letterSpacing: "1px" }}>Update Profile Data</h3>

                                    <div className="form-outline mb-4">
                                        <label for="updateProductName" className="form-label">Full Name</label>
                                        <input type="text" id="updateProductName" className="form-control form-control-lg" placeholder={userData.full_name} value={fullname} onChange={(e) => setFullName(e.target.value)} />
                                    </div>

                                    <div className="form-outline mb-4">
                                        <label for="updateProductDescription" className="form-label">Password</label>
                                        <input type="text" id="updateProductDescription" className="form-control form-control-lg" placeholder="Place if you want to change" value={password} onChange={(e) => setPassword(e.target.value)} />
                                    </div>

                                    <div className="form-outline mb-4">
                                        <label for="updateStartingAmount" className="form-label">Email</label>
                                        <input type="text" id="updateStartingAmount" className="form-control form-control-lg" placeholder={userData.email} value={email} onChange={(e) => setEmail(e.target.value)} />
                                    </div>

                                    <div className="form-outline mb-4">
                                        <input type="file" className="form-control form-control-lg" onChange={(e) => setImage(e.target.files[0])} />
                                    </div>

                                    <ErrorMessage message={errorMessage} />

                                    <div className="pt-1 mt-3 mb-4">
                                        <button className="btn btn-info btn-lg btn-block text-light" type="submit">Update Data</button>
                                    </div>
                                </form>
                            </div>
                        </div>
                        <div className="col-sm-6 my-5">
                            <div className="container">
                                {console.log(userData.profile_pic.url)}
                                <img src={userData.profile_pic.url ? "http://localhost:8000" + userData.profile_pic.url : "https://dummyimage.com/300x200/000/fff"} alt="User Profile Pic Display" className="img-fluid" />
                            </div>
                        </div>
                    </div>)}
            </div>
        </section>
    )
}