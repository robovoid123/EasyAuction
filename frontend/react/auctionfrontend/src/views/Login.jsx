const Login = () => {
    return (
        <section className="vh-90">
            <div className="container mt-4">
                <div className="row">
                    <div className="col-sm-6 text-black">
                        <div className="d-flex align-items-center h-custom-2 px-5 ms-xl-4 mt-5 pt-5 pt-xl-0 mt-xl-n5">
                            <form style={{ width: "23rem" }}>
                                <h3 className="fw-normal mb-3 pb-3" style={{ letterSpacing: "1px" }}>Log in</h3>

                                <div className="form-outline mb-4">
                                    <input type="email" className="form-control form-control-lg" placeholder="Email" />
                                </div>

                                <div className="form-outline mb-4">
                                    <input type="password" className="form-control form-control-lg" placeholder="Password" />
                                </div>

                                <div className="pt-1 mb-4">
                                    <button className="btn btn-info btn-lg btn-block text-light" type="button">Login</button>
                                </div>

                                <p className="small mb-5 pb-lg-2"><a class="text-muted" href="#!">Forgot password?</a></p>
                                <p>Don't have an account? <a href="signup" className="link-info">Register here</a></p>
                            </form>
                        </div>
                    </div>
                    <div className="col-sm-6 px-0 d-none d-sm-block">
                        <img src="https://dummyimage.com/600x700/000/fff" alt="dummy" className="w-100" style={{ objectFit: "cover", objectPosition: "left" }} />
                    </div>
                </div>
            </div>
        </section>
    )
}

export default Login