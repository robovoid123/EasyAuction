import FeaturedList from "../components/FeaturedList"
import LiveAuction from "../components/LiveAuction"
import banner from "../assets/img/banner.png"

const HomePage = () => {
    return (
        <div>
            <div className="container mt-2">
                <img src={banner} className="img-fluid" alt="banner" />
            </div>
            <FeaturedList />
            <div className="container mt-4">
                <hr />
            </div>
            <LiveAuction />
        </div>
    )
}

export default HomePage
