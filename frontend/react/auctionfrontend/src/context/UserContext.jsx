import React, { createContext, useEffect, useState } from "react";

export const UserContext = createContext();

export const UserProvider = (props) => {
  const [token, setToken] = useState(localStorage.getItem("userLoginToken"));
  const [userId, setUserId] = useState(localStorage.getItem("userId"))

  useEffect(() => {
    localStorage.setItem("userLoginToken", token);
    const fetchUser = async () => {
      const requestOption =  {
        headers: {
            "Content-Type": "application/json",
            Authorization: "bearer " + token,
        },
        mode: 'cors',
      }

      const response = await fetch("/api/v1/users/me", requestOption)
      const data = await response.json()

      localStorage.setItem("userId", data.id);
    }
    fetchUser()

  }, [token]);

  return (
    <UserContext.Provider value={{ token:[token, setToken], userData:[userId, setUserId]}}>
      {props.children}
    </UserContext.Provider>
  );
};