import SearchIcon from "@material-ui/icons/Search";
import { useState } from "react";
import { Link } from "react-router-dom";

const SearchNav = props => {
    const [search, setSearch] = useState("")

    return (
        <form className="d-flex" id="FORM" autoComplete="off">
            <input className="form-control" type="search" placeholder="Search" aria-label="Search" value={search} onChange={(e) => setSearch(e.target.value)}/>
            <Link to={{
                pathname: 'searchResult',
                state: search,
            }}>
                <button className="btn btn-outline-primary" type="submit"><SearchIcon/></button>
            </Link>
        </form>
    )
}

export default SearchNav
