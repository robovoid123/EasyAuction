import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { DeleteProduct } from '../components/DeleteProduct'

const Product = () => {

    const [products, setProducts] = useState([])

    useEffect(() => {
        fetch(`/api/v1/products/users/104?skip=0&limit=5`, { mode: 'cors' })
            .then((response) => response.json())
            .then((json) => {
                setProducts(json)
            })
    }, [])

    return (
        <div className="container">
            <h1 className="my-3 border-bottom border-3">Product Management</h1>
            <a href="productAdd" className="btn btn-info mb-4 text-light">Add Product</a>
            {products.map((product) => (
                <div className="row" key={product.id}>
                    <div className="col-lg-8 mx-auto">
                        <ul className="list-group shadow">
                            <li className="list-group-item">
                                <div class="media align-items-lg-center flex-column flex-lg-row p-3">
                                    <div class="media-body order-2 order-lg-1">
                                        <h5 class="mt-0 font-weight-bold mb-2">{product.name}</h5>
                                        <p class="font-italic text-muted mb-0 small">{product.description}</p>
                                        <h6 class="font-weight-bold my-2">Current_bid</h6>
                                        <div className="d-flex">
                                            <Link to={{
                                                pathname: 'productUpdate',
                                                state: product.id,
                                            }}>
                                                <button className="btn btn-info me-2 my-2 text-light">Update Product</button>
                                            </Link>
                                            <DeleteProduct id={product.id} />
                                        </div>
                                    </div>
                                    <img src={(product.images.length) >= 1 ? "http://localhost:8000" + product.images[product.images.length - 1].url : "https://dummyimage.com/300x200/000/fff"} alt="Product Display" width="200" class="ml-lg-5 order-1 order-lg-2" />
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
            ))}
        </div>
    )
}

export default Product
