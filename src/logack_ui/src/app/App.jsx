import { useEffect } from "react"
import { BrowserRouter, Routes, Route, useNavigate } from "react-router"

import { UserProvider, useUser } from "./api/user.jsx"

/**
 * Initialize Application
 */
const Init = () => {
    const navigate = useNavigate();
    const user = useUser();
    
    // Check if we are authenticated. If not, show signup.
    useEffect(() => {
        console.log(user);
        if( !user.loading && user.is_anonymous ) {
            navigate("/session/signin", {
                replace: true,
            });
        } else {
            navigate("/events", {
                replace: true,
            });
        }
    }, [user]);

    return <div>Div</div>;
}

const SignInView = () => {
    const user = useUser();
    console.log(user);
    return <div>Sign In</div>;
}

const EventsView = () => {
    const user = useUser();
    console.log(user);
    return <div>[...events...]</div>;
}


/**
 * Application Main
 */
const App = () => {
    return (
        <UserProvider>
        <BrowserRouter>
            <Routes>
                <Route
                    path="/" 
                    element={<Init />} />
                <Route
                    path="/session/signin"
                    element={<SignInView />} />
                <Route
                    path="/events"
                    element={<EventsView />} />
            </Routes>
        </BrowserRouter>
        </UserProvider>
    );
};


export default App;

