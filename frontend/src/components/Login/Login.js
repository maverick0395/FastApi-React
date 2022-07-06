import { useForm } from "react-hook-form";
import { useState } from "react";

import { userService } from "../../services";
import css from "./Login.module.css";

const Login = () => {
    const [response, setResponse] = useState({
        "okMessage": "",
        "errorMessage": "",
    })

    const {
        handleSubmit, register
    } = useForm();

    const submit = async (formData) => {
        // const userData = {
        //     "username": formData.username,
        //     "password": formData.password
        // }

        const userData = new FormData();
        userData.append("username", formData.username);
        userData.append("password", formData.password);

        try {
            const token = await userService.loginUser(userData).then(value => value.data);
            if (token) {
                localStorage.setItem('APIToken', token.access_token);
                console.log(token);
            }
            setResponse({okMessage: "User has been logged in"})
        } catch (e) {
            setResponse({errorMessage: e.message})
        }
    }

    return (
        <div>
            {response.okMessage && <div className={css.okMessage}>{response.okMessage}</div>}
            {response.errorMessage && <div className={css.errorMessage}>{response.errorMessage}</div>}
            <form onSubmit={handleSubmit(submit)} className={css.form}>
                <p>
                    <label>Username</label>
                    <input type="text" {...register('username')} />
                </p>
                <p>
                    <label>Password</label>
                    <input type="password" {...register('password')} />
                </p>
                <button>Register</button>
            </form>
        </div>
    );
};

export {Login};