import React from "react";
import { Link } from 'react-router-dom'

const ProductIndiButton = () => {
    return (
        <div>
            <Link to={'item'}>
                <button type="button" className="btn px-3 me-2 btn-primary">Bid on item</button>
            </Link>
        </div>
    )
}

export default ProductIndiButton
