import React, { useContext, useEffect, useState } from "react"
import SearchNav from "./SearchNav"
import { UserContext } from "../context/UserContext"
import { Link } from "react-router-dom"
import AccessAlarmIcon from '@material-ui/icons/NotificationsActiveSharp';

const Nav = () => {
    const [UserDataMe, setUserDataMe] = useState()
    const [notifications, setNotifications] = useState([])
    const [isLoading, setIsLoading] = useState(true)
    const { token, userData } = useContext(UserContext)


    useEffect(() => {

        const fetchNotification = async () => {
            const requestNotification = {
                method: 'GET',
                headers: {
                    Authorization: "bearer " + token[0]
                },
                mode: 'cors',
            }

            const responseNotification = await fetch("/api/v1/notification/me", requestNotification)
            const dataNotification = await responseNotification.json()


            if (responseNotification.ok) {
                setNotifications(dataNotification)
            }
        }

        const fetchUser = async () => {
            const requestUserMe = {
                method: 'GET',
                headers: {
                    Authorization: "bearer " + token[0],
                },
                mode: 'cors',
            }

            const response = await fetch("/api/v1/users/me", requestUserMe)
            const data = await response.json()

            if (response.ok) {
                setUserDataMe(data)
                await fetchNotification()
                setIsLoading(false)
            }

        }


        fetchUser()
    }, [])



    const handleLogout = () => {
        token[1](null)
    }

    const a = [1, 2, 3]

    return (
        <nav className="navbar navbar-expand-md navbar-light bg-light mb-4">
            <div className="container py-2">
                <div>
                    <a href="/" className="navbar-brand">EasyAuction</a>
                </div>
                <button className="navbar-toggler mb-3 mt-2" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse flex-row-reverse" id="navbarNav">
                    <div className="navbar-nav">
                        <SearchNav />
                        {token[0] === 'null' || !token[0] ? (
                            <>
                                <a href="login" className="btn btn-link px-3 me-2 nav-link">Login</a>
                                <a href="signup" className="btn btn-info me-3 nav-link text-light">Sign up</a>
                            </>
                        ) : (
                            <>
                                {isLoading ? <div className="spinner-border text-info" role="status"></div> : (
                                    <ul className="navbar-nav mb-2 mb-lg-0">
                                        <li class="nav-item dropdown">
                                            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                                <AccessAlarmIcon />
                                                <span class="badge rounded-pill badge-notification bg-danger">
                                                    {notifications ? <>{notifications.length}</> : <>0</>}
                                                </span>
                                            </a>
                                            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                                                {console.log(notifications, !notifications)}
                                                {notifications ? <>{notifications.map(notification => <li>{notification.title}</li>)}</> :
                                                    <li><a href="biditemlist" className="nav-link text-muted">No Notification</a></li>
                                                }
                                            </ul>
                                        </li>
                                        <li class="nav-item dropdown">
                                            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                                <img src={UserDataMe.profile_pic.url !== "" ? "http://localhost:8000" + UserDataMe.profile_pic.url : "https://dummyimage.com/300x200/000/fff"} alt="User Profile Pic Display" className="rounded-circle" height="30" width="30" loading="lazy" />
                                            </a>

                                            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                                                <li><a href="biditemlist" className="nav-link text-muted">BidItemList</a></li>
                                                <li><a href="product" className="nav-link text-muted">AuctionManagement</a></li>
                                                <li><a href="settings" className="nav-link text-muted">Settings</a></li>
                                                <li><hr class="dropdown-divider" /></li>
                                                <li>
                                                    <Link to={{
                                                        pathname: '/',
                                                    }}>
                                                        <button className="btn text-muted" onClick={handleLogout}>Logout</button>
                                                    </Link>
                                                </li>
                                            </ul>
                                        </li>
                                    </ul>)}
                            </>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    )
}

export default Nav