import SearchIcon from "@material-ui/icons/Search";

const SearchNav = () => {
    return (
        <form className="d-flex">
            <input className="form-control" type="search" placeholder="Search" aria-label="Search" />
            <button className="btn btn-outline-primary" type="submit"><SearchIcon className="" /></button>
        </form>
    )
}

export default SearchNav
