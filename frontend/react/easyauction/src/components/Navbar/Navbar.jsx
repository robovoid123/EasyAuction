import React from 'react'

const Navbar = () => (
    <section class='heading-section'>
        <div class="container-fluid login-bar">
            <div class="">
                <a href="">Login in</a> / <a href="">Register</a>
            </div>
        </div>
        <nav class="navbar navbar-dark bg-dark py-4">
            <div class="container d-flex flex-column flex-sm-row">
                <div class="mb-2 mb-sm-0">
                    <a class="navbar-brand ">Auction System</a>
                </div>
                <form class="d-flex flex-grow-1 px-sm-4">
                    <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" />
                    <button class="btn btn-outline-success" type="submit">Search</button>
                </form>
            </div>
        </nav>
    </section>
)

export default Navbar