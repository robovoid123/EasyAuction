import React, { useContext, useState } from 'react'
import { UserContext } from '../context/UserContext'

export const StartAuction = ({id}) => {
    const {token} = useContext(UserContext)
    const [startingDate, setStartingDate] = useState()
    const [endingDate, setEndingDate] = useState()

    const startAuction = async ()=> {
        const resquestOption = {
            method: "POST",
            headers : {
                "Content-Type": "application/json",
                Authorization: "bearer" + token[0],
            },
            body: JSON.stringify({
                "starting_date": startingDate,
                "ending_date": endingDate
            }),
            mode: 'cors'
        }

        const response = await fetch(`/api/v1/auctions/${id}/start`, resquestOption)
        const data = await response.json()
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        startAuction()
    }

    return (
        <>
            <button type="button" class="btn btn-info mx-2 my-2 text-light" data-bs-toggle="modal" data-bs-target="#staticBackdrop"> Start Auction </button>

            <div className="modal fade" id="staticBackdrop" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div className="modal-dialog modal-dialog-centered">
                <div className="modal-content">
                <div className="modal-header">
                    <h5 className="modal-title" id="exampleModalLabel">Start Auction</h5>
                    <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form style={{ width: "23rem" }} onSubmit={handleSubmit}>
                    <div className="modal-body">
                            <div className="form-outline mb-4">
                                <input type="date" className="form-control form-control-lg" placeholder="Starting Date" value={startingDate} onChange={(e) => setStartingDate(e.target.value)} />
                            </div>

                            <div className="form-outline mb-4">
                                <input type="date" className="form-control form-control-lg" placeholder="Ending Date" value={endingDate} onChange={(e) => setEndingDate(e.target.value)} />
                            </div>

                            {/* <ErrorMessage message={errorMessage} /> */}
                    </div>
                    <div className="modal-footer">
                        <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button className="btn btn-info mx-2 my-2 text-light" type="submit">Start Auction</button>
                    </div>
                </form>
                </div>
            </div>
            </div>
        </>
    )
}
