import { axiosService } from "./";
import baseURL from "../constants/urls";

export const userService = {
    registerUser: (registrationData) => axiosService.post(`${baseURL}/register`, registrationData),
    loginUser: (loginData) => axiosService.post(`${baseURL}/login`, loginData)
}