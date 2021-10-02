import React from "react";
import { Link } from 'react-router-dom'

const ProductIndiButton = ({id}) => {
    return (
        <div>
            <Link to={{
                pathname: '/item', 
                state: id,
            }}>
                <button type="button" className="btn px-3 me-2 btn-primary">Bid on item</button>
            </Link>
        </div>
    )
}

export default ProductIndiButton
