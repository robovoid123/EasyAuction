import React, { useContext, useState } from "react";
import { UserContext } from "../context/UserContext";
import { ErrorMessage } from "../components/ErrorMessage";
import imageSignup from "../assets/img/auctionBid.png"

const Signup = props => {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [fullname, setFullname] = useState("")
    const [image, setImage] = useState("")
    const [errorMessage, setErrorMessage] = useState("")
    const {token} = useContext(UserContext)

    const submitRegistration = async () => {

        const formData = new FormData()
        const headers = {}
        formData.append('password', password)
        formData.append('email', email)
        formData.append('full_name', fullname)
        formData.append('image', image)

        headers.Accept = 'application/json'

        const requestOptions = {
            method: 'POST',
            headers,
            body: formData,
            mode: 'cors',
        }

        const response = await fetch("/api/v1/users/register", requestOptions)
        const data = await response.json()

        if (!response.ok) {
            let responseErrorMessage = data.detail
            // if error message from backend is a string then only set ErrorMessage
            // TODO: error message which are object need to be handled seperately
            if (typeof (responseErrorMessage) !== 'string') {
                responseErrorMessage = ''
            }
            setErrorMessage(responseErrorMessage)
        } else {
            token[1](data.access_token)
            props.history.push("login")
        }
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        if (password.length > 8 && image != null) {
            submitRegistration()
        } else {
            setErrorMessage(
                "Ensure the password is greate than 8 character and profile pic is uploaded"
            )
        }
    }

    return (
        <section className="vh-90">
            <div className="container mt-4">
                <div className="row">
                    <div className="col-sm-6 px-0 d-none d-sm-block">
                        <img src={imageSignup} alt="Auction Bid" className="w-100" style={{ objectFit: "cover", objectPosition: "left" }} />
                    </div>
                    <div className="col-sm-6 text-black">
                        <div className="d-flex align-items-center h-custom-2 px-5 ms-xl-4 mt-5 pt-5 pt-xl-0 mt-xl-n5">
                            <form style={{ width: "23rem" }} onSubmit={handleSubmit}>
                                <h3 className="fw-normal mb-3 pb-3" style={{ letterSpacing: "1px" }}>Signup</h3>

                                <div className="form-outline mb-4">
                                    <input type="username" className="form-control form-control-lg" placeholder="Full Name" value={fullname} onChange={(e) => setFullname(e.target.value)} />
                                </div>

                                <div className="form-outline mb-4">
                                    <input type="email" className="form-control form-control-lg" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
                                </div>

                                <div className="form-outline mb-4">
                                    <input type="password" className="form-control form-control-lg" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                                </div>

                                <div className="form-outline mb-4">
                                    <input type="file" className="form-control form-control-lg" onChange={(e) => setImage(e.target.files[0])} />
                                </div>

                                <ErrorMessage message={errorMessage} />

                                <div className="pt-1 mt-3 mb-4">
                                    <button className="btn btn-info btn-lg btn-block text-light" type="submit">Signup</button>
                                </div>

                                <p>Already have an account? <a href="login" className="link-info">Login here</a></p>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default Signup