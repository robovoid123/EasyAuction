import React, { useState, useContext } from "react"

import { ErrorMessage } from '../components/ErrorMessage'
import { UserContext } from '../context/UserContext'
import imageLogin from '../assets/img/auctionPhone.png'

const Login = props => {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [errorMessage, setErrorMessage] = useState("")
    const { token } = useContext(UserContext)

    const submitLogin = async () => {
        const requestOptions = {
            method: 'POST',
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: JSON.stringify(
                `grant_type=&username=${email}&password=${password}&scope=&client_id=&client_secret=`
            ),
            mode: 'cors',
        }

        const response = await fetch('/api/v1/auth/access-token', requestOptions)
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
            props.history.push('/')
        }
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        submitLogin()
    }

    return (
        <section className="vh-90">
            <div className="container mt-4">
                <div className="row">
                    <div className="col-sm-6 text-black">
                        <div className="d-flex align-items-center h-custom-2 px-5 ms-xl-4 mt-5 pt-5 pt-xl-0 mt-xl-n5">
                            <form style={{ width: "23rem" }} onSubmit={handleSubmit}>
                                <h3 className="fw-normal mb-3 pb-3" style={{ letterSpacing: "1px" }}>Log in</h3>

                                <div className="form-outline mb-4">
                                    <input type="email" className="form-control form-control-lg" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
                                </div>

                                <div className="form-outline mb-4">
                                    <input type="password" className="form-control form-control-lg" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                                </div>

                                <ErrorMessage message={errorMessage} />

                                <div className="pt-1 mb-4">
                                    <button className="btn btn-info btn-lg btn-block text-light" type="submit">Login</button>
                                </div>

                                <p className="small mb-5 pb-lg-2"><a className="text-muted" href="#!">Forgot password?</a></p>
                                <p>Don't have an account? <a href="signup" className="link-info">Register here</a></p>
                            </form>
                        </div>
                    </div>
                    <div className="col-sm-6 px-0 d-none d-sm-block">
                        <img src={imageLogin} alt="dummy" className="w-100" style={{ objectFit: "cover", objectPosition: "left" }} />
                    </div>
                </div>
            </div>
        </section>
    )
}

export default Login