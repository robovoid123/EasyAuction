import React from 'react'

export const AddAuction = () => {
    return (
        <div>
            <button type="button" class="btn btn-info text-light me-2 my-2" data-bs-toggle="modal" data-bs-target="#staticBackdrop">Add to Auction</button>

            <div class="modal fade" id="staticBackdrop" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="staticBackdropLabel">Add Product to Auction</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <form style={{ width: "23rem" }}>
                                <div className="form-outline mb-4">
                                    <input type="text" className="form-control form-control-lg" placeholder="Starting Date" required/>
                                </div>

                                <div className="form-outline mb-4">
                                    <input type="text" className="form-control form-control-lg" placeholder="Ending Date" required/>
                                </div>

                                {/* <ErrorMessage message={errorMessage} /> */}
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-primary">Confirm</button>
                        </div>
                    </div>
                </div>
            </div>
    
        </div>
    )
}
