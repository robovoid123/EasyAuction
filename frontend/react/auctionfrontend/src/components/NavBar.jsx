import SearchNav from "./SearchNav"

const Nav = () => {
    return (
        <nav className="navbar navbar-expand-md navbar-light bg-light">
            <div className="container">
                <a href="/" className="navbar-brand">EasyAuction</a>
                <button class="navbar-toggler mb-3 mt-2" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                        <li class="nav-item">
                            <a class="nav-link" href="/">Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="about">About</a>
                        </li>
                    </ul>
                    <div className="navbar-nav">
                        <SearchNav />
                        <a href="login" className="btn btn-link px-3 me-2 nav-link">Login</a>
                        <a href="signup" className="btn btn-info me-3 nav-link text-light">Sign up</a>
                    </div>
                </div>
            </div>
        </nav>
    )
}

export default Nav