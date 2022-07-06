import { Route, Routes } from "react-router-dom"

import { Header, Login, Register } from "./components";

function App() {
  return (
    <>
      <Routes>
        <Route path={'/'} element={<Header/>}>
          <Route path={'register'} element={<Register/>}/>
          <Route path={'login'} element={<Login/>}/>
        </Route>
      </Routes>
    </>
  );
}

export default App;
