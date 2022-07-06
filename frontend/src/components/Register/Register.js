import { useForm } from "react-hook-form";
import { useState } from "react";

import { userService } from "../../services";
import css from "./Register.module.css";

const Register = () => {
    const [response, setResponse] = useState({
        "okMessage": "",
        "errorMessage": "",
    })

    const {
        handleSubmit, register
    } = useForm();

    const submit = async (formData) => {
        const userData = {
            "username": formData.username,
            "email": formData.email,
            "password": formData.password
        }
    
        try {
            await userService.registerUser(userData).then(value => value.data);
            setResponse({okMessage: "User has been registered"});
        } catch (e) {
            setResponse({errorMessage: e.message});
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
                    <label>Email</label>
                    <input type="text" {...register('email')} />
                </p>
                <p>
                    <label>Password</label>
                    <input type="password" {...register('password')} />
                </p>
                <button>Register</button>
            </form>
        </div>
    )
}

export {Register};

