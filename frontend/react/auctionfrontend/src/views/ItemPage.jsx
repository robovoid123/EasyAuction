import React from "react";

const ItemPage = ({id}) => {
    return (
        <div className="container mt-5">
            <div className="row">
                <div className="col-md-6">
                    <img src="https://dummyimage.com/600x400/000/fff" className="img-fluid " alt="dummy" />
                </div>
                <div className="col-md-6">
                    <div className="row">
                        <div className="col-md-12 mt-2">
                            <h1>Product Name</h1>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-md-12">
                            <span className="btn btn-info me-4">CateTag</span>
                            <span className="monospaced">ProductId</span>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-md-12 mt-3">
                            <h5>Owner Name</h5>
                            <p>However, the same kind of thinking can be positively applied to marketing. Just remember that little, tiny things which often don’t get directly considered by the conscious mind can have a big impact on whether or not visitors to you.</p>
                        </div>
                    </div>
                    <div className="row">
                        <h4>Starting Bid:- $100</h4>
                        <h4>Current Bid:- $123</h4>
                        <h5>Ending Date:- 2021/08/08</h5>
                    </div>
                    <div className="row">
                        <div className="col-md-6 mt-3">
                            <input type="text" className="form-control" placeholder="Enter price to bid" />
                        </div>
                        <div className="col-md-6 mt-3">
                            <button className="btn btn-info">Bid</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default ItemPage