import {NavLink, Outlet} from "react-router-dom";

import css from "./Header.module.css"

const Header = () => {
    return (
        <>
            <div className={css.header_wrapper}>
                <NavLink to="/">Home</NavLink>
                <NavLink to="/register">Register</NavLink>
                <NavLink to="/login">Log In</NavLink>
            </div>
            <Outlet/>
        </>
    );
};

export {Header};