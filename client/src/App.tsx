import React from 'react';
import './App.css';
import {Link, Route, Router, Routes} from "react-router-dom";
import {HomePage} from "./pages/home";
import {MergerPage} from "./pages/merger";

function App() {
  return (
      <div>
          <nav>
              <ul>
                  <li>
                      <Link to="/">Home</Link>
                  </li>
                  <li>
                      <Link to="/merger">Merger</Link>
                  </li>
              </ul>
          </nav>

          <Routes>
              <Route path="/merger" element={<MergerPage />} />
              <Route path="/" element={<HomePage />} />
          </Routes>
      </div>
  );
}

export default App;
