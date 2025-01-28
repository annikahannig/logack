
import { useEffect, useState, createContext, useContext } from "react"

import { get, post } from "./request"

export const UserContext = createContext();
export const useUser = () => useContext(UserContext);

/**
 * Initial state of the user context
 */
const defaultUser = {
    loading: true,
    id: null,
    username: "",
    first_name: "",
    last_name: "",
    is_anonymous: true,
};

/**
 * API
 */
async function apiGetUser() {
    return await get("/api/v1/user/");
}

async function apiCreateUser(data) {
    return await post("/api/v1/user/", data);
}

/**
 * Provide the user context.
 */
export const UserProvider = ({children}) => {
    const [user, setUser] = useState(defaultUser);

    // Fetch the current user
    useEffect(() => {
        apiGetUser().then((user) => {
            user.loading = false;
            setUser(user);
        });
    }, []);

    return (
        <UserContext.Provider value={user}>
            {children}
        </UserContext.Provider>
    );
}


