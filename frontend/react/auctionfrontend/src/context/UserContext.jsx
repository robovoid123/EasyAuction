import React, { createContext, useEffect, useState } from "react";

export const UserContext = createContext();

export const UserProvider = (props) => {
  const [token, setToken] = useState(localStorage.getItem("userLoginToken"));

  useEffect(() => {
    // const fetchUser = async () => {
    // const requestOptions = {
    // method: "GET",
    // headers: {
    // "Content-Type": "application/json",
    // Authorization: "Bearer " + token,
    // },
    // mode: "cors",
    // };

    // const response = await fetch("/api/v1/auth/access-token", requestOptions);

    // if (!response.ok) {
    //   setToken(null);
    // }
    // };
    localStorage.setItem("userLoginToken", token);

  }, [token]);

  return (
    <UserContext.Provider value={[token, setToken]}>
      {props.children}
    </UserContext.Provider>
  );
};